import datetime

from fastapi import FastAPI

from fastapi_rss import (
    RSSFeed, RSSResponse, Item, Category,
    CategoryAttrs, GUID,
)

app = FastAPI()


@app.get('/')
async def root():
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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app2:app', host='127.0.0.1', port=8081, log_level='info')
