from pydantic import BaseModel


class TextInput(BaseModel):
    title: str
    description: str
    name: str
    link: str
