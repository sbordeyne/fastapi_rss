from typing import Optional

from pydantic import BaseModel


class GUIDAttrs(BaseModel):
    is_permalink: bool


class GUID(BaseModel):
    content: str
    attrs: Optional[GUIDAttrs] = None
