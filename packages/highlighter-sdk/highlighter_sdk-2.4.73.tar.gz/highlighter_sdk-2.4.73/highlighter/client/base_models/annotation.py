from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union
from uuid import UUID, uuid4

import numpy as np
import shapely.geometry as geom
from PIL.Image import Image
from pydantic import BaseModel, ConfigDict, Field, field_validator

from highlighter.core.hl_base_model import HLModelMap

from ...core import OBJECT_CLASS_ATTRIBUTE_UUID, BelongsTo, HasMany, HLDataModel
from .base_models import EAVT
from .data_file import DataFile
from .datum_source import DatumSource
from .observation import Observation

__all__ = ["Annotation"]


class AnnotationCrop(BaseModel):
    content: Any
    annotation_id: UUID
    entity_id: Optional[UUID] = None


@HasMany("observations", target_cls="highlighter.client.Observation", back_populates="annotation")
@BelongsTo(
    "entity",
    target_cls="highlighter.client.Entity",
    back_populates="annotations",
)
class Annotation(HLDataModel):
    id: UUID = Field(..., default_factory=uuid4)
    entity_id: Optional[UUID] = None
    location: Optional[Union[geom.Polygon, geom.MultiPolygon, geom.LineString, geom.Point]] = None
    observations: HLModelMap = Field(..., default_factory=lambda: HLModelMap(Observation))
    # TODO update HL Web to refer to data-sources (e.g. webrtc streams) as well as files
    track_id: Optional[UUID] = None
    data_file_id: Optional[UUID] = None
    correlation_id: Optional[UUID] = None

    datum_source: DatumSource

    model_config = ConfigDict(arbitrary_types_allowed=True)  # Required for shapely geometry types

    def serialize(self):
        return {
            "id": str(self.id),
            "entity_id": str(self.entity_id),
            "location": self.location.wkt if self.location is not None else None,
            "observations": [o.serialize() for o in self.observations.values()],
            "track_id": str(self.track_id),
            "correlation_id": str(self.correlation_id),
            "data_file_id": str(self.data_file_id),
            "datum_source": self.datum_source.serialize(),
        }

    def get_observation(self, attribute_id: UUID) -> Optional[Observation]:
        for o in self.observations:
            if o.attribute_id == attribute_id:
                return o
        return None

    def has_observation(self, attribute_id: UUID, value: Optional[Any] = None) -> bool:
        if value is None:
            return any([o.attribute_id == attribute_id for o in self.observations])
        else:
            return any([((o.attribute_id == attribute_id) and (o.value == value)) for o in self.observations])

    def crop(self, crop_args: "CropArgs") -> AnnotationCrop:
        from ...datasets.cropping import crop_rect_from_poly

        if self.data_file_id is None:
            raise ValueError("Cannot crop an Annotation when data_file_id is None")
        if self.location is None:
            raise ValueError("Cannot crop an Annotation when location is None")
        if not isinstance(self.location, geom.Polygon):
            raise ValueError(f"Cannot crop an Annotation when location is {type(self.location)}")

        data_file = DataFile.find_by_id(self.data_file_id)

        if data_file is None:
            raise ValueError(f"Could not find DataFile with id {self.data_file_id}")

        if "image" not in data_file.content_type:
            raise ValueError(
                f"Cannot crop data_file with content_type '{data_file.content_type}', must be 'image'"
            )

        if not isinstance(data_file.content, (np.ndarray, Image)):
            raise ValueError(
                f"Cannot crop data_file with content '{type(data_file.content)}', must be (PIL.Image|np.array)"
            )

        cropped_image = crop_rect_from_poly(data_file.content, self.location, crop_args)
        return AnnotationCrop(content=cropped_image, entity_id=self.entity_id, annotation_id=self.id)

    def to_deprecated_pixel_location_eavt(self) -> EAVT:
        return EAVT.make_pixel_location_eavt(
            entity_id=self.entity_id,
            location_points=self.location,
            confidence=self.datum_source.confidence,
            time=datetime.now(timezone.utc),
            frame_id=self.datum_source.frame_id,
        )

    @field_validator("location")
    @classmethod
    def validate_geometry(cls, v):
        if v is not None:
            assert v.is_valid, f"Invalid Geometry: {v}"
        return v

    def to_json(self):
        data = self.model_dump()
        data["id"] = str(data["id"])
        data["entity_id"] = str(data["entity_id"])
        data["location"] = data["location"].wkt
        data["datum_source"] = data["datum_source"]
        data["observations"] = [d.to_json() for d in data["observations"].values()]

        data["track_id"] = str(data["track_id"]) if self.track_id is not None else None
        data["data_file_id"] = str(data["track_id"]) if self.track_id is not None else None
        data["correlation_id"] = str(data["track_id"]) if self.track_id is not None else None
        return data

    def gql_dict(self) -> Dict:
        try:
            object_class_observation = [
                observation
                for observation in self.observations
                if observation.attribute_id == OBJECT_CLASS_ATTRIBUTE_UUID
            ][-1]
        except IndexError:
            raise ValueError(
                "Annotation must have an object-class observation in order to submit to Highlighter"
            )

        if isinstance(self.location, geom.Polygon):
            data_type = "polygon"
        elif isinstance(self.location, geom.LineString):
            data_type = "line"
        elif isinstance(self.location, geom.Point):
            data_type = "point"
        else:
            data_type = "polygon"
        result = {
            "objectClassUuid": str(object_class_observation.value),
            "location": self.location.wkt if self.location is not None else None,
            "confidence": self.datum_source.confidence,
            "dataType": data_type,
            "correlationId": str(self.correlation_id),
            "frameId": self.datum_source.frame_id,
            "trackId": self.track_id,
            "entityId": str(self.entity_id),
            "dataFileId": str(self.data_file_id),
            "uuid": str(self.id),
        }
        return result
