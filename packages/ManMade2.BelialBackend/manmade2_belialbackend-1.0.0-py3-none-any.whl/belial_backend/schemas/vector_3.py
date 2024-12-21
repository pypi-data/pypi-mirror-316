from pydantic import BaseModel


class Vector3(BaseModel):
    x: float
    y: float
    z: float

    class Config:
        from_attributes = True
