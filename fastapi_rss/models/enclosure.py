from typing import Optional

from pydantic import BaseModel


class EnclosureAttrs(BaseModel):
    url: Optional[str] = None
    length: Optional[int] = None
    type: Optional[str] = None


class Enclosure(BaseModel):
    attrs: EnclosureAttrs
