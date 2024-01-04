from datetime import datetime
from email.utils import format_datetime
from typing import Any, Dict, List, Optional, Union

from fastapi import __version__ as faversion
from lxml import etree
from pydantic import BaseModel, Field

from fastapi_rss import __version__ as farssversion
from fastapi_rss.models.category import Category
from fastapi_rss.models.cloud import Cloud
from fastapi_rss.models.image import Image
from fastapi_rss.models.item import Item
from fastapi_rss.models.textinput import TextInput
from fastapi_rss.utils import get_locale_code, to_camelcase


class RSSFeed(BaseModel):
    title: str
    link: str
    description: str

    language: Optional[str] = get_locale_code()
    copyright: Optional[str] = None
    managing_editor: Optional[str] = None
    webmaster: Optional[str] = None
    pub_date: Optional[datetime] = None
    last_build_date: Optional[datetime] = None
    category: Optional[List[Category]] = Field(default_factory=list)
    generator: str = f'FastAPI v{faversion} w/ FastAPI_RSS v{farssversion}'
    docs: str = 'https://validator.w3.org/feed/docs/rss2.html'
    cloud: Optional[Cloud] = None
    ttl: int = 60
    image: Optional[Image] = None
    text_input: Optional[TextInput] = None
    skip_hours: List[int] = Field(default_factory=list)
    skip_days: List[str] = Field(default_factory=list)

    item: List[Item] = Field(default_factory=list)

    @staticmethod
    def _get_attrs(value: Union[dict, BaseModel]) -> Dict[str, str]:
        '''
        Gets attrs from value, keys are passed to camel case and values to str

        :return: Attrs as dictionary
        '''
        attrs = None
        if hasattr(value, 'attrs'):
            attrs = value.attrs.dict()
        elif 'attrs' in value:
            attrs = value['attrs']

        attrs = attrs or {}

        # if boolean then string in lower case
        return {
            to_camelcase(k): str(v).lower() if isinstance(v, bool) else str(v)
            for k, v in attrs.items()
        }

    @classmethod
    def _generate_tree_list(cls, root: etree.ElementBase, key: str,
                            value: List[dict]) -> None:
        for item in value:
            attrs = cls._get_attrs(item)
            content = item.pop('content', None)
            itemroot = etree.SubElement(root, key, attrs)
            if content is not None:
                itemroot.text = content
            else:
                cls.generate_tree(itemroot, item)

    @classmethod
    def _generate_tree_object(cls, root: etree.ElementBase, key: str,
                              value: Union[dict, BaseModel]) -> None:
        attrs = cls._get_attrs(value)
        if hasattr(value, 'content'):
            content = value.content
        elif 'content' in value:
            content = value['content']
        else:
            content = None

        if key == 'itunes':
            # Used for podcast image
            etree.SubElement(
                root, '{http://www.itunes.com/dtds/podcast-1.0.dtd}image',
                attrs,
            )
            return

        element: etree.ElementBase = etree.SubElement(root, key, attrs)
        if content:
            element.text = content

    @staticmethod
    def _generate_tree_default(root: etree.ElementBase, key: str, value: Any) -> None:
        element: etree.ElementBase = etree.SubElement(root, key)
        if isinstance(value, datetime):
            # parse datetime as specified in RFC 2822
            value = format_datetime(value)
        else:
            value = str(value)
        element.text = value

    @classmethod
    def generate_tree(cls, root: etree.Element, dict_: dict):
        handlers = {
            (list,): cls._generate_tree_list,
            (BaseModel, dict): cls._generate_tree_object,
        }
        for key, value in dict_.items():
            if value is None:
                continue
            handler = cls._generate_tree_default
            for handler_types, _handler in handlers.items():
                if isinstance(value, handler_types):
                    handler = _handler
                    break
            handler(root, to_camelcase(key), value)

    def tostring(self, nsmap: Optional[Dict[str, str]] = None):
        nsmap = nsmap or {}
        rss = etree.Element('rss', version='2.0', nsmap=nsmap)
        channel = etree.SubElement(rss, 'channel')
        self.generate_tree(channel, self.dict())
        return etree.tostring(rss, pretty_print=True, xml_declaration=True)
