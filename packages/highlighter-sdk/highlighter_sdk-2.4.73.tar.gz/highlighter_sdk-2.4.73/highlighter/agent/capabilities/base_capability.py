from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, List, Literal, Optional, Tuple, Union
from uuid import UUID

import aiko_services as aiko
from aiko_services import (
    PROTOCOL_PIPELINE,
    PipelineImpl,
    compose_instance,
    pipeline_args,
    pipeline_element_args,
)
from aiko_services.elements.media.common_io import DataSource as BaseDataSource
from pydantic import BaseModel

from highlighter.client import DataFile
from highlighter.client.io import (
    _pil_open_image_bytes,
    download_bytes,
    read_image,
    read_image_from_url,
)

__all__ = [
    "Capability",
    "DataSourceCapability",
    "ContextPipelineElement",
    "EntityUUID",
    "PROTOCOL_PIPELINE",
    "PipelineElement",
    "PipelineImpl",
    "StreamEvent",
    "compose_instance",
    "compose_instance",
    "pipeline_args",
    "pipeline_element_args",
]

EntityUUID = UUID

"""Decouple the rest of the code from aiko.PipelineElement"""
ContextPipelineElement = aiko.ContextPipelineElement
StreamEvent = aiko.StreamEvent
PipelineElement = aiko.PipelineElement

# SEPARATOR = b"\x1c"  # ASCII 28 (File Separator)
SEPARATOR = 28  # ASCII 28 (File Separator)


class _BaseCapability:
    class DefaultStreamParameters(BaseModel):
        """Populate with default stream param key fields"""

        pass

    @classmethod
    def default_stream_parameters(cls) -> BaseModel:
        return {
            k: v.default for k, v in cls.DefaultStreamParameters.model_fields.items() if not v.is_required()
        }

    def _get_parameter(self, name, default=None, use_pipeline=True) -> Tuple[Any, bool]:
        """Adds the correct output type to get_parameter type checking
        does not complain
        """
        return self.get_parameter(name, default, use_pipeline)


class Capability(PipelineElement, _BaseCapability):

    def __init__(self, context: aiko.ContextPipelineElement):
        context.get_implementation("PipelineElement").__init__(self, context)

    def process_frame(self, stream, *args) -> Tuple[StreamEvent, Optional[Dict]]:
        raise NotImplementedError()

    def start_stream(self, stream, stream_id, use_create_frame=True):
        validated_parameters = self.DefaultStreamParameters(**self.parameters)
        for param_name in self.DefaultStreamParameters.model_fields:
            self.parameters[f"{self.definition.name}.{param_name}"] = getattr(
                validated_parameters, param_name
            )
            self.parameters.pop(param_name, None)
        stream.parameters.update(self.parameters)
        return StreamEvent.OKAY, {}


class DataSourceType(BaseModel):
    # class MediaType(str, Enum):
    #    IMAGE = "IMAGE"
    #    TEXT = "TEXT"
    #    VIDEO = "VIDEO"

    media_type: str
    url: str
    id: UUID
    content: Optional[Any] = None

    @classmethod
    def image_iter(cls, images: Iterable[Union[str, Path, bytes]]):
        pass

    @classmethod
    def video_iter(cls, videos: Iterable[Union[str, Path, bytes]]):
        pass

    @classmethod
    def text_iter(cls, tests: Iterable[Union[str, Path, bytes]]):
        pass


class DataSourceCapability(BaseDataSource, _BaseCapability):
    """DataSourceCapabilities can either:

        - create one frame for one file:   ONE_TO_ONE  (eg: data_files)
        - create many frames for one file: ONE_TO_MANY (eg: videos)

    This is defined by the`files_to_frames` class variable.

    DataSourceCapability developers should implement the `bytes_to_frame_data` and
    `filepath_to_frame_data` functions

    """

    stream_media_type = None

    class DefaultStreamParameters(_BaseCapability.DefaultStreamParameters):

        rate: Optional[float] = None
        batch_size: int = 1
        data_sources: List[DataSourceType] = []
        file_ids: Optional[Iterable] = None
        task_id: Optional[UUID] = None

    @property
    def rate(self) -> float:
        return self._get_parameter("rate")[0]

    @property
    def batch_size(self) -> int:
        return self._get_parameter("batch_size")[0]

    def __init__(self, context: aiko.ContextPipelineElement):
        context.get_implementation("PipelineElement").__init__(self, context)
        self._STOP = False

    def frame_batch_generator(self, stream, pipeline_iter_idx):
        """Produce a batch of frames.

        Args:
            stream: The Stream context
            pipeline_iter_idx: An integer counting the number of times the
                               pipeline has been executed, (ie: process_frame
                               has been called)

        """
        if self._STOP:
            return StreamEvent.STOP, {"diagnostic": "All frames generated"}

        batch_size = self.batch_size
        task_id, _ = self._get_parameter("task_id")

        frame_data_batch = defaultdict(list)
        for _ in range(batch_size):
            frame_data_gen = stream.variables["frame_data_generator"]
            try:
                frame_data = next(frame_data_gen)
            except StopIteration:
                break

            self.logger.debug(f"frame_data: {frame_data}")

            # Convert list of dicts to dict or lists
            # [{"data_files": ..., "entities": ...}, ...]
            # {"data_files": [...], "entities": [...]}
            for k, v in frame_data.items():
                frame_data_batch[k].append(v)

        # For each pipeline iteration the is a batch of file_ids and frame_ids
        stream.variables["task_id"] = task_id

        if len(frame_data_batch):
            return StreamEvent.OKAY, frame_data_batch
        else:
            return StreamEvent.STOP, {"diagnostic": "All frames generated"}

    def frame_data_generator(self, data_sources):
        pass

    def start_stream(self, stream, stream_id, use_create_frame=True):
        data_sources, _ = self._get_parameter("data_sources")

        if not data_sources:
            raise ValueError("data_sources is empty")

        if getattr(self, "stream_media_type", None) is None:
            raise ValueError(
                "All subclasses of DataSourceCapability, must have "
                "'stream_media_type' set as a class variable"
            )

        stream.variables["stream_media_type"] = self.stream_media_type
        stream.variables["frame_data_generator"] = self.frame_data_generator(data_sources)

        self.create_frames(stream, self.frame_batch_generator, rate=self.rate)
        return StreamEvent.OKAY, {}

    def process_frame(self, stream, data_files: List[str], entities) -> Tuple[StreamEvent, Dict]:
        return StreamEvent.OKAY, {"data_files": data_files, "entities": entities}

    def stop_stream(self, stream, stream_id) -> Tuple[StreamEvent, Optional[str]]:
        self.stop()
        return StreamEvent.OKAY, {}
