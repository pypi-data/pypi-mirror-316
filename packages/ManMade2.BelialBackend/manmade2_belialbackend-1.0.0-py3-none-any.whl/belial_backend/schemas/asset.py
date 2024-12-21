from pydantic import BaseModel

from .vector_3 import Vector3
from .vector_4 import Vector4


class AssetSchema(BaseModel):
    id: int
    path: str
    type: str
    scale_factor: float
    position: Vector3
    rotation: Vector4

    class Config:
        from_attributes = True
