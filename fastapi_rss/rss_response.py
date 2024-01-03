import hashlib
from typing import Mapping

from starlette.responses import Response

from fastapi_rss.models import RSSFeed


class RSSResponse(Response):
    '''
    A subclass of starlette.responses.Response which will set the content
    to an RSS XML document. It takes one argument, an RSSFeed object which will
    be converted to an XML document.
    '''
    media_type = 'application/xml'
    charset = 'utf-8'

    @property
    def etag(self) -> str:
        '''
        Generates a SHA1 sum of the body of the response so that the server can
        support the ETag protocol.

        :return: The SHA1 hex digest of the body of the response
        :rtype: str
        '''
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

    def render(self, rss: RSSFeed, itunes: bool = False) -> bytes:
        nsmap = None
        if itunes:
            nsmap = {
                'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'
            }
        return rss.tostring(nsmap)
