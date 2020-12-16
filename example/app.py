import datetime

from fastapi import FastAPI
from fastapi_rss import (
    RSSFeed, RSSResponse, Item, Category, CategoryAttrs,
)


app = FastAPI()


@app.get('/rss')
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


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('app:app', host='127.0.0.1', port=8080, log_level='info')
