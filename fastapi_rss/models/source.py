from pydantic import BaseModel


class SourceAttrs(BaseModel):
    url: str


class Source(BaseModel):
    content: str
    attrs: SourceAttrs
