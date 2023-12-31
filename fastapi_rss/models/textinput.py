from typing import Optional

from pydantic import BaseModel


class TextInput(BaseModel):
    title: Optional[str]
    description: Optional[str]
    name: Optional[str]
    link: Optional[str]
