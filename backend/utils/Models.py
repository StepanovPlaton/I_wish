from typing import TypedDict
from pydantic import BaseModel


class AuthorizationDataModel(BaseModel):
    Login: str
    Password: str

class SuccessAuthorizationModel(BaseModel):
    Token: str

class UserInDatabaseModel(TypedDict):
    ID: int
    Login: str
    HashOfPassword: str