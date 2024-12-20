import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

from highlighter.client import HLJSONEncoder

from .base_capability import Capability, ContextPipelineElement, StreamEvent

__all__ = [
    "EntityWriteFile",
    "WriteStdOut",
]


class BaseEntityWrite(Capability):

    class DefaultStreamParameters(Capability.DefaultStreamParameters):
        task_id: str = ""

    def __init__(self, context: ContextPipelineElement):
        super().__init__(context)
        self.frame_entities = dict()

    def get_task_id(self, stream) -> str:
        return stream.variables.get("task_id", None)

    def _get_source_file_location(self, stream):
        # ToDo: Find a better palce to put/get this from
        #       see also, ImageDataSource.process_frame
        source_info = stream.variables.get("source_info", {})
        source_file_location = source_info.get("source_file_location", None)
        if source_file_location is not None:
            return Path(source_file_location)
        return None

    def on_per_frame(self, stream, entities):
        pass

    def process_frame(self, stream, entities) -> Tuple[StreamEvent, Optional[Dict]]:
        self.on_per_frame(stream, entities)
        self.frame_entities[stream.frame_id] = entities
        return StreamEvent.OKAY, {}

    def on_stop_stream(self, stream, stream_id, entities):
        """Note this will not be called if you're calling `pipeline.process_frame`
        directly. Because this is called when a stream is stopped
        """
        pass

    def stop_stream(self, stream, stream_id) -> Tuple[StreamEvent, Optional[Dict]]:
        self.on_stop_stream(stream, stream_id, self.frame_entities)
        return StreamEvent.OKAY, {}


class EntityWriteFile(BaseEntityWrite):

    class DefaultStreamParameters(BaseEntityWrite.DefaultStreamParameters):
        """Can contain the following placeholders:

            {frame_id}
            {task_id}
            {timestamp}

        for example:
            per_frame_output_file = 'output_{frame_id}_{timestamp}.json'
        """

        per_frame_output_file: Optional[str] = None

        """Can contain the following placeholders:

            {task_id}
            {timestamp}
        """
        stop_stream_output_file: Optional[str] = None

    @property
    def per_frame_output_file(self) -> Optional[str]:
        value, _ = self._get_parameter("per_frame_output_file", None)
        return value

    @property
    def stop_stream_output_file(self) -> Optional[str]:
        value, _ = self._get_parameter("stop_stream_output_file", None)
        return value

    def get_per_frame_output_file_path(self, stream):
        task_id = stream.stream_id
        frame_id = stream.frame_id

        return self.per_frame_output_file.format(
            frame_id=frame_id,
            task_id=task_id,
            timestamp=datetime.now().strftime("%Y%m%d%H%M%S%f"),
        )

    def on_per_frame(self, stream, entities):
        if self.per_frame_output_file:
            output_file_path = self.get_per_frame_output_file_path(stream)
            Path(output_file_path).parent.mkdir(exist_ok=True, parents=True)
            with open(output_file_path, "w") as f:
                f.write(json.dumps(entities, indent=2, sort_keys=True, cls=HLJSONEncoder))
                self.logger.debug(f"{self.my_id()}: wrote {len(entities)} entities to {output_file_path} ")

    def get_on_stop_stream_output_file_path(self, stream):
        task_id = stream.variables.get("task_id", None)
        return self.stop_stream_output_file.format(
            stream_id=stream.stream_id,
            task_id=task_id,
        )

    def on_stop_stream(self, stream, stream_id, all_entities):
        if self.stop_stream_output_file:
            self.logger.debug(f"Writing stop_stream_output_file: {self.stop_stream_output_file}")
            output_file_path = self.get_on_stop_stream_output_file_path(stream)
            Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file_path, "w") as f:
                f.write(json.dumps(all_entities, indent=2, sort_keys=True, cls=HLJSONEncoder))


class WriteStdOut(BaseEntityWrite):

    def on_per_frame(self, stream, entities):

        for entity in entities:
            output = {"frame_data": entity, "frame_id": stream.frame_id}
            print(json.dumps(output), file=sys.stdout, cls=HLJSONEncoder)
