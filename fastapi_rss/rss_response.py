import hashlib
from typing import Mapping

from fastapi_rss.models import RSSFeed

from starlette.responses import Response


class RSSResponse(Response):
    media_type = 'application/xml'
    charset = 'utf-8'

    @property
    def etag(self):
        return hashlib.sha1(self.body).hexdigest()

    def init_headers(self, headers: Mapping[str, str] = None) -> None:
        newheaders = {
            'Accept-Range': 'bytes',
            'Connection': 'Keep-Alive',
            'ETag': self.etag,
            'Keep-Alive': 'timeout=5, max=100',
        }

        headers = headers or {}
        for headername in newheaders:
            if headername not in headers:
                headers[headername] = newheaders[headername]
        super().init_headers(headers)

    def render(self, rss: RSSFeed) -> bytes:
        return rss.tostring()
