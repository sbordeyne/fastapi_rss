from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    title: str
    link: str

    width: Optional[int]
    height: Optional[int]
    description: Optional[str]
