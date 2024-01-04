from typing import Optional

from pydantic import BaseModel


class ItunesAttrs(BaseModel):
    href: str


class Itunes(BaseModel):
    content: str
    attrs: Optional[ItunesAttrs] = None
