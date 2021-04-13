import datetime
from typing import Optional

from pydantic import BaseModel

from fastapi_rss.models.category import Category
from fastapi_rss.models.enclosure import Enclosure
from fastapi_rss.models.guid import GUID
from fastapi_rss.models.source import Source
from fastapi_rss.models.itunes import Itunes


class Item(BaseModel):
    title: str
    link: Optional[str]
    description: Optional[str]
    author: Optional[str]
    category: Optional[Category]
    comments: Optional[str]
    enclosure: Optional[Enclosure]
    guid: Optional[GUID]
    pub_date: Optional[datetime.datetime]
    source: Optional[Source]
    itunes: Optional[Itunes]
