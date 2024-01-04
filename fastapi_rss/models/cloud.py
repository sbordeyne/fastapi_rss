from typing import Optional

from pydantic import BaseModel


class CloudAttrs(BaseModel):
    domain: Optional[str] = None
    port: Optional[str] = None
    path: Optional[str] = None
    register_procedure: Optional[str] = None
    protocol: Optional[str] = None


class Cloud(BaseModel):
    attrs: Optional[CloudAttrs] = None
