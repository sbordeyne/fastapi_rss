from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    title: str
    link: str

    width: Optional[int] = None
    height: Optional[int] = None
    description: Optional[str] = None
