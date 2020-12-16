from typing import Optional

from pydantic import BaseModel


class CategoryAttrs(BaseModel):
    domain: Optional[str]


class Category(BaseModel):
    content: str
    attrs: Optional[CategoryAttrs]
