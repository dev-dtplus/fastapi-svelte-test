from pydantic import BaseModel, validator


class DeviceCreate(BaseModel):
    place: int


class Device(BaseModel):
    id: int

    class Config:
        orm_mode = True


# class DeviceUpdate(BaseModel):
#     auth_id: int