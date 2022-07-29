from typing import TypedDict
from pydantic import BaseModel

# --- User authorization ---

class AuthorizationDataModel(BaseModel):
    Login: str
    Password: str

class SuccessAuthorizationResponseModel(BaseModel):
    ID: int
    Token: str

class SuccessRegistrationResponseModel(BaseModel):
    ID: int
    Token: str

class TokenRequestBodyModel(BaseModel):
    Token: str

class CheckTokenResponse(BaseModel):
    TokenCorrect: bool

# --- Wishes ---

class WishesRequestBodyModel(BaseModel):
    Token: str
    Wish: str
    Image: str | None
    Description: str | None
    Price: int | None
    Link: str | None

class UserRequestBodyModel(BaseModel):
    Token: str
    Avatar: str | None
    AboutMe: str | None
    Telegram: str | None

class Owner(TypedDict):
    ID: int
    Login: str
    Avatar: str

class WishIDModel(BaseModel):
    ID: int

# --- Database ---

class UserInDatabaseModel(TypedDict):
    ID: int
    Login: str
    HashOfPassword: str
    Avatar: str | None
    AboutMe: str | None
    Telegram: str | None

class UserInDatabaseWithoutPasswordModel(TypedDict):
    ID: int
    Login: str
    Avatar: str | None
    AboutMe: str | None
    Telegram: str | None

class WishesDatabaseModel(TypedDict):
    ID: int
    Wish: str
    Image: str | None
    Description: str | None
    Price: int | None
    Link: str | None
    Owner: int
    Login: str
    Avatar: str | None