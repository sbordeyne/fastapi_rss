from typing import Optional

from pydantic import BaseModel


class EnclosureAttrs(BaseModel):
    url: str
    length: int
    type: str


class Enclosure(BaseModel):
    content: str
    attrs: Optional[EnclosureAttrs]
