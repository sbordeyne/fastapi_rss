from datetime import datetime
from typing import Any, Dict, Optional, List, Union

from fastapi import __version__ as faversion
from lxml import etree
from pydantic import BaseModel

from fastapi_rss import __version__ as farssversion
from fastapi_rss.utils import get_locale_code, to_camelcase
from fastapi_rss.models.category import Category
from fastapi_rss.models.cloud import Cloud
from fastapi_rss.models.image import Image
from fastapi_rss.models.textinput import TextInput
from fastapi_rss.models.item import Item


class RSSFeed(BaseModel):
    title: str
    link: str
    description: str

    language: str = get_locale_code()
    copyright: Optional[str]
    managing_editor: Optional[str]
    webmaster: Optional[str]
    pub_date: Optional[datetime]
    last_build_date: Optional[datetime]
    category: Optional[List[Category]]
    generator: str = f'FastAPI v{faversion} w/ FastAPI_RSS v{farssversion}'
    docs: str = 'https://validator.w3.org/feed/docs/rss2.html'
    cloud: Optional[Cloud]
    ttl: int = 60
    image: Optional[Image]
    text_input: Optional[TextInput]
    skip_hours: List[int] = []
    skip_days: List[str] = []

    item: List[Item] = []

    @staticmethod
    def _generate_tree_list(root: etree.Element, key: str, value: List[dict]) -> None:
        for item in value:
            attrs = item.pop('attrs', {})
            content = item.pop('content', None)
            itemroot = etree.SubElement(root, to_camelcase(key), attrs)
            if content is not None:
                itemroot.text = content
            else:
                RSSFeed.generate_tree(itemroot, item)

    @staticmethod
    def _generate_tree_object(root: etree._Element, key: str, value: Union[dict, BaseModel]) -> None:
        if hasattr(value, 'attrs'):
            attrs = value.attrs.dict()
        elif 'attrs' in value:
            attrs = value['attrs']
            if attrs is not None and 'length' in attrs:
                # overriding length to be a string, because SubElement ( first below )
                # doesn't like ints ( i.e. length of podcast in an int )
                attrs['length'] = str(attrs['length'])
        else:
            attrs = {}

        if hasattr(value, 'content'):
            content = value.content
        elif 'content' in value:
            content = value['content']
        else:
            content = None

        if key == 'itunes':
            # Used for podcast image
            element: etree._Element = etree.SubElement(
                root, '{http://www.itunes.com/dtds/podcast-1.0.dtd}image',
                attrs,
            )
            return

        element: etree._Element = etree.SubElement(root, to_camelcase(key), attrs)
        if content:
            element.text = content

    @staticmethod
    def _generate_tree_datetime(root: etree._Element, key: str, value: datetime) -> None:
        value = value.strftime('%a, %d %b %Y %H:%M:%S GMT')
        element: etree._Element = etree.SubElement(root, to_camelcase(key))
        element.text = str(value)

    @staticmethod
    def _generate_tree_default(root: etree._Element, key: str, value: Any) -> None:
        element: etree._Element = etree.SubElement(root, to_camelcase(key))
        element.text = str(value)

    @staticmethod
    def generate_tree(root: etree.Element, dict_: dict):
        handlers = {
            (list, ): RSSFeed._generate_tree_list,
            (BaseModel, dict): RSSFeed._generate_tree_object,
            (datetime, ): RSSFeed._generate_tree_datetime
        }
        for key, value in dict_.items():
            if value is None:
                continue
            for handler_types, handler in handlers.items():
                if isinstance(value, handler_types):
                    handler(root, key, value)
                    break
            else:
                RSSFeed._generate_tree_default(root, key, value)

    def tostring(self, nsmap: Optional[Dict[str, str]] = None):
        nsmap = nsmap or {}
        rss = etree.Element('rss', version='2.0', nsmap=nsmap)
        channel = etree.SubElement(rss, 'channel')
        RSSFeed.generate_tree(channel, self.dict())
        return etree.tostring(rss, pretty_print=True, xml_declaration=True)
