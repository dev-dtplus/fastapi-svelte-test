from pydantic import BaseModel, validator


class PlaceCreate(BaseModel):
    name: str
    address: str
    number: str

    @validator('name', 'address', 'number')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

# class Place(Base):
#     __tablename__ = "place"

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     address = Column(String, nullable=False)
#     number = Column(String, nullable=False)


# class UserCreate(BaseModel):
#     username: str
#     password1: str
#     password2: str
#     email: EmailStr

#     @validator('username', 'password1', 'password2', 'email')
#     def not_empty(cls, v):
#         if not v or not v.strip():
#             raise ValueError('빈 값은 허용되지 않습니다.')
#         return v

#     @validator('password2')
#     def passwords_match(cls, v, values):
#         if 'password1' in values and v != values['password1']:
#             raise ValueError('비밀번호가 일치하지 않습니다')
#         return v

class Place(BaseModel):
    id: int
    name: str
    address: str
    number: str
    
    class Config:
        orm_mode = True