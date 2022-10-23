from pydantic import BaseModel


class EnclosureAttrs(BaseModel):
    url: str
    length: int
    type: str


class Enclosure(BaseModel):
    attrs: EnclosureAttrs
