import datetime
from textwrap import dedent

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from fastapi_rss import (
    Enclosure, EnclosureAttrs, GUIDAttrs, RSSFeed, RSSResponse, Item, Category,
    CategoryAttrs, GUID,
)


@fixture
def expected_response():
    return dedent('''\
        <?xml version='1.0' encoding='ASCII'?>
        <rss version="2.0">
        <channel>
            <title>Scripting News</title>
            <link>http://www.scripting.com/</link>
            <description>A weblog about scripting and stuff like that.</description>
            <language>en-us</language>
            <copyright>Copyright 1997-2002 Dave Winer</copyright>
            <managingEditor>dave@userland.com</managingEditor>
            <webmaster>dave@userland.com</webmaster>
            <lastBuildDate>Mon, 30 Sep 2002 11:00:00 +0000</lastBuildDate>
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
        ''')


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
                guid=GUID(
                    content='abcdefghijklmnopqrstuvwxyz',
                    attrs=GUIDAttrs(is_permalink=False)
                ),
                enclosure=Enclosure(attrs=EnclosureAttrs(
                    url="https://example.com/",
                    length=125,
                    type="audio/mpeg"
                ))
            )
        ],
    }
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)


@fixture
def client():
    app = FastAPI()
    app.get('/1')(first)
    app.get('/2')(second)
    return TestClient(app)
