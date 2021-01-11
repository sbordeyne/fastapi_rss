import unittest

import datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_rss import (
    RSSFeed, RSSResponse, Item, Category,
    CategoryAttrs, GUID,
)
from lxml import etree


expected_response = '''\
<rss version="2.0">
  <channel>
    <title>Scripting News</title>
    <link>http://www.scripting.com/</link>
    <description>A weblog about scripting and stuff like that.</description>
    <language>en-us</language>
    <copyright>Copyright 1997-2002 Dave Winer</copyright>
    <managingEditor>dave@userland.com</managingEditor>
    <webmaster>dave@userland.com</webmaster>
    <lastBuildDate>Mon, 30 Sep 2002 11:00:00 GMT</lastBuildDate>
    <category domain="Syndic8">1765</category>
    <generator>Radio UserLand v8.0.5</generator>
    <docs>http://backend.userland.com/rss</docs>
    <ttl>40</ttl>
    <item>
      <title>First item</title>
    </item>
    <item>
      <title>Second item</title>
    </item>
    <item>
      <title>Third item</title>
    </item>
  </channel>
</rss>
'''.encode('utf8')


async def first():
    feed_data = {
        'title': 'Scripting News',
        'link': 'http://www.scripting.com/',
        'description': 'A weblog about scripting and stuff like that.',
        'language': 'en-us',
        'copyright': 'Copyright 1997-2002 Dave Winer',
        'last_build_date': datetime.datetime(2002, 9, 30, 11, 0, 0),
        'docs': 'http://backend.userland.com/rss',
        'generator': 'Radio UserLand v8.0.5',
        'category': [Category(
            content='1765', attrs=CategoryAttrs(domain='Syndic8')
        )],
        'managing_editor': 'dave@userland.com',
        'webmaster': 'dave@userland.com',
        'ttl': 40,
        'item': [
            Item(title='First item'),
            Item(title='Second item'),
            Item(title='Third item')
        ]
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)


async def second():
    feed_data = {
        'title': 'Test 2',
        'link': '',
        'description': "",
        'language': 'en-us',
        'copyright': 'Copyright',
        'last_build_date': datetime.datetime(
            year=2021, month=1, day=11,
            hour=2, minute=49, second=32
        ),
        'managing_editor': 'self@example.com',
        'webmaster': 'self@example.com',
        'generator': 'Test',
        'ttl': 30,
        'item': [
            Item(
                title='Test',
                link='https://www.example.com/projects/2020/12/31/test',
                description='',
                author='Dogeek',
                category=Category(
                    content='0001',
                    attrs=CategoryAttrs(domain='test')
                ),
                pub_date=datetime.datetime(
                    year=2020, month=12, day=31,
                    hour=12, minute=40, second=16,
                ),
                guid=GUID(content='abcdefghijklmnopqrstuvwxyz')
            )
        ],
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)


class TestRSSResponse(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()

        self.app.get('/1')(first)
        self.app.get('/2')(second)

        self.client = TestClient(self.app)

    def assertXPathExists(self, tree, xpath):
        self.assertNotEqual(tree.xpath(xpath), [])

    def assertXPathAttrEquals(self, tree, xpath, attr, expected):
        el = tree.xpath(xpath)[0]
        self.assertEqual(el.attrib[attr], expected)

    def assertXPathContentEquals(self, tree, xpath, expected):
        el = tree.xpath(xpath)[0]
        self.assertEqual(el.text, expected)

    def test_rss_sample_response(self):
        response = self.client.get('/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_response)

    def test_rss_guid(self):
        response = self.client.get('/2')
        tree = etree.fromstring(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertXPathExists(tree, '//guid')
        self.assertXPathContentEquals(
            tree, '//guid', 'abcdefghijklmnopqrstuvwxyz'
        )

    def test_rss_item_category(self):
        response = self.client.get('/2')
        tree = etree.fromstring(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertXPathExists(tree, '//category')
        self.assertXPathAttrEquals(tree, '//category', 'domain', 'test')
        self.assertXPathContentEquals(tree, '//category', '0001')
