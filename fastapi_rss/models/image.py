from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    url: Optional[str]
    title: Optional[str]
    link: Optional[str]

    width: Optional[int]
    height: Optional[int]
    description: Optional[str]
