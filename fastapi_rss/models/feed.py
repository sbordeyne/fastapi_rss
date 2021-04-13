from datetime import datetime
from typing import Optional, List

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
    def generate_tree(root, dict_):  # TODO: improve that shiete
        for key, value in dict_.items():
            if value is None:
                continue
            if isinstance(value, list):
                for item in value:
                    attrs = item.pop('attrs', {})
                    content = item.pop('content', None)
                    itemroot = etree.SubElement(root, to_camelcase(key), attrs)
                    if content is not None:
                        itemroot.text = content
                    else:
                        RSSFeed.generate_tree(itemroot, item)
                continue

            if isinstance(value, BaseModel) or isinstance(value, dict):
                if hasattr(value, 'attrs'):
                    attrs = value.attrs.dict()
                elif 'attrs' in value:
                    attrs = value['attrs']
                    if 'length' in attrs:
                        # overriding length to be a string, because SubElement ( first below )
                        #   doesn't like ints ( i.e. length of podcast in an int )
                        attrs['length'] = str(attrs['length'])
                else:
                    attrs = {}

                if hasattr(value, 'content'):
                    content = value.content
                elif 'content' in value:
                    content = value['content']
                else:
                    content = None

                # used for podcast image
                if key == 'itunes':
                    element = etree.SubElement( root, '{http://www.itunes.com/dtds/podcast-1.0.dtd}image', attrs)
                    continue

                element = etree.SubElement(root, to_camelcase(key), attrs)
                if content:
                    element.text = content
                continue

            if isinstance(value, datetime):
                value = value.strftime('%a, %d %b %Y %H:%M:%S GMT')
            element = etree.SubElement(root, to_camelcase(key))
            element.text = str(value)

    def tostring(self):
        nsmap = {
            'itunes': "http://www.itunes.com/dtds/podcast-1.0.dtd"
        }
        rss = etree.Element('rss', version='2.0', nsmap=nsmap)
        channel = etree.SubElement(rss, 'channel')
        RSSFeed.generate_tree(channel, self.dict())
        return etree.tostring(rss, pretty_print=True)
