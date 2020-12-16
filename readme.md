# FastAPI RSS

A library to easily integrate RSS Feeds into FastAPI

## Rationale

The RSS standard has been around for a long time, and the specification has not
changed much in the past 20 years. Regardless, it is still a useful format, and
there is an added value to have an automated feed for updates about an API
(notify users of upcoming changes), or in general as a backend for full-featured
applications


## Usage

You will need to import at least three classes to use that library:

- `RSSResponse`, which is a subclass of `starlette.Response`. It's a `text/xml` typed response which will handle generating the XML from the pydantic models
- `RSSFeed` which is a pydantic model that represents an RSS feed according to the `RSS v2.0` specification from the **World Wide Web Consortium**
- `Item` which is another pydantic model that represents an item in the feed.

Once those are imported, instanciate an `RSSFeed` object, with the appropriate parameters, then return an `RSSResponse` with that feed.

Your endpoint should now return an appropriate XML document representing your RSS feed.
Look at example/app.py for an example app that uses the **W3C** RSS example.
