from typing import Optional

from pydantic import BaseModel


class CloudAttrs(BaseModel):
    domain: Optional[str]
    port: Optional[str]
    path: Optional[str]
    register_procedure: Optional[str]
    protocol: Optional[str]


class Cloud(BaseModel):
    attrs: Optional[CloudAttrs]
