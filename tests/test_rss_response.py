import unittest

import datetime
from unittest.case import expectedFailure

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_rss import (
    RSSFeed, RSSResponse, Item, Category, CategoryAttrs,
)


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


async def root():
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


class TestRSSResponse(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()

        self.app.get('/')(root)
        self.client = TestClient(self.app)

    def test_rss_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, expected_response)
