from typing import Optional

from pydantic import BaseModel


class SourceAttrs(BaseModel):
    url: Optional[str]


class Source(BaseModel):
    content: Optional[str]
    attrs: SourceAttrs
