from typing import Optional

from pydantic import BaseModel


class ItunesAttrs(BaseModel):
    href: Optional[str]


class Itunes(BaseModel):
    content: Optional[str]
    attrs: Optional[ItunesAttrs]
