from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str


class LoginUser(BaseModel):
    username: str
    password: str


class UpdateUser(BaseModel):
    firstname: str
    password: str


