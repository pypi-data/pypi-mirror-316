from typing import Any, Optional
from uuid import UUID

from ...core import HLDataModel

__all__ = ["DataFile"]


class DataFile(HLDataModel):
    file_id: UUID
    content_type: str
    content: Any
    media_frame_index: int = 0
    original_source_url: Optional[str] = None

    def get_id(self) -> UUID:
        return self.file_id
