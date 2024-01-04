import inspect
from importlib.metadata import version
from typing import TYPE_CHECKING

import pytest
from pydantic import BaseModel

if TYPE_CHECKING:
    from pydantic.fields import ModelField

pydantic_major = int(version('pydantic').split('.')[0])
if pydantic_major >= 2:
    from pydantic_core import PydanticUndefined
else:
    from pydantic.fields import UndefinedType as PydanticUndefined

from fastapi_rss.models import (
    Category, CategoryAttrs,
    Image,
    ItunesAttrs, Itunes,
    Cloud, CloudAttrs,
    Item,
    TextInput,
    Enclosure, EnclosureAttrs,
    GUID, GUIDAttrs,
    Source, SourceAttrs,
    RSSFeed
)

MODELS = [i for i in locals().values() if inspect.isclass(i) and issubclass(i, BaseModel)]


@pytest.mark.parametrize('model',MODELS)
def test_optionals_have_defaults(model):
    if pydantic_major >= 2:
        fields = model.model_fields
    else:
        fields = model.__fields__

    field: 'ModelField'
    for name, field in fields.items():
        if not field.required:
            assert field.field_info.default is not PydanticUndefined


def test_instantiate_optionals():
    feed = RSSFeed(
        title="My Feed",
        link="https://example.com",
        description="A feed!"
    )
    item = Item(
        title="My Item"
    )