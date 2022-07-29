#!/usr/bin/python

from fastapi import FastAPI, HTTPException
import uvicorn #type: ignore

from utils.YAMLReader import YAMLReaderClass
from utils.ConfigReader import ConfigClass
from utils.Logger import LoggerClass
from utils.DatabaseFriend import *
from utils.Hasher import HasherClass
from utils.Models import *



YAMLReader = YAMLReaderClass()
Config = ConfigClass(YAMLReader)
Logger = LoggerClass(Config)
Hasher = HasherClass()
DatabaseFriend: DatabaseFriendClass | None = None

app = FastAPI()

@app.on_event("startup") #type: ignore
async def startup():
    global DatabaseFriend

    Logger.Log("Server startup - OK")
    DatabaseFriend = DatabaseFriendClass(Config, Logger, Hasher)
    if(not await DatabaseFriend.DatabaseInit()):
        raise DatabaseConnectionFailed()

@app.post("/authorization", response_model=SuccessAuthorizationResponseModel)
async def Authorization(Login: str, Password: str):
    Logger.Log(f"Authorization attempt with login - {Login}", 1)
    if(DatabaseFriend):
        try: 
            Authorized = await DatabaseFriend.\
                        CheckUserAuthorizationData(Login, Password)
        except DatabaseFriendCheckAuthorizationDataError:
            raise HTTPException(
                status_code=500, 
                detail="Verify user authorization data impossible. "\
                        "Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            raise HTTPException(
                status_code=404, 
                detail="Verify user authorization data impossible. "\
                        "User not found."
            )
        else:
            if(Authorized):
                Logger.Log(f"User with login - {Login}, authorized", 2)
                try:
                    UserID = (await DatabaseFriend.GetUserWithoutPasswordByLogin(Login))["ID"]
                except DatabaseFriendGetUserByLoginError:
                    raise HTTPException(
                        status_code=500, 
                        detail="Authorization impossible. Database access error."
                    )
                else:
                    return { 
                        "Token": Hasher.GetToken(Login, \
                                        Hasher.HashOfPassword(Password)),
                        "ID": UserID
                    }
            else:
                Logger.Log(f"Authorization denied for user with login {Login}"\
                                                " - wrong login or password", 3)
                raise HTTPException(
                    status_code=404, 
                    detail="Authorization data wrong. Check you login and password."
                )
    Logger.Log(f"Unusual turn of events during authorization", 2)
    raise HTTPException(status_code=500)

@app.post("/registration", response_model=SuccessRegistrationResponseModel)
async def Registration(Login: str, Password: str):
    Logger.Log(f"Registration attempt with login - {Login}", 1)
    if(DatabaseFriend):
        try:
            Logger.Log(f"Check the login ({Login}) is free before registation user", 1)
            LoginIsFree = await DatabaseFriend.CheckLoginIsFree(Login)
        except DatabaseFriendCheckLoginIsFreeError:
            raise HTTPException(
                status_code=500, 
                detail="Verify new login is free impossible. "\
                        "Database access error."
            )
        else:
            if(LoginIsFree):
                try:
                    await DatabaseFriend.RegistrationNewUser(Login, Password)
                except DatabaseFriendRegistrationNewUserError:
                    Logger.Log(f"Registration with login ({Login}) failed "\
                                                    "Database error", 4)
                    raise HTTPException(
                        status_code=500, 
                        detail="Registration impossible. Database access error."
                    )
                else: 
                    Logger.Log(f"User with login - {Login}, registered", 2)
                    try:
                        UserID = (await DatabaseFriend.GetUserWithoutPasswordByLogin(Login))["ID"]
                    except DatabaseFriendGetUserByLoginError:
                        raise HTTPException(
                            status_code=500, 
                            detail="Registration impossible. Database access error."
                        )
                    else:
                        return { 
                            "Token": Hasher.GetToken(Login, \
                                            Hasher.HashOfPassword(Password)),
                            "ID": UserID
                        }
            else:
                Logger.Log(f"Login ({Login}) busy. Registation user impossible", 3)
                raise HTTPException(
                    status_code=409, 
                    detail="The selected username is already taken"
                )
    Logger.Log(f"Unusual turn of events during registration", 3)
    raise HTTPException(status_code=500)

@app.post("/check_token", response_model=CheckTokenResponse)
async def CheckToken(Login: str, Body: TokenRequestBodyModel):
    Logger.Log(f"User {Login} trying check token", 1)
    if(DatabaseFriend):
        try:
            TokenCorrect = await DatabaseFriend.CheckToken(Login, Body.Token)
        except DatabaseFriendCheckTokenError:
            Logger.Log(f"Check token of user {Login} failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't check token. Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            Logger.Log(f"Check token of user {Login} failed. User not found", 4)
            raise HTTPException(
                status_code=404, 
                detail="Can't check token. User not found."
            )
        else:
            if(TokenCorrect):
                Logger.Log(f"Token of user {Login} correct", 2)
                return {
                    "TokenCorrect": True
                }
            else:
                Logger.Log(f"Token of user {Login} incorrect", 3)
                return {
                    "TokenCorrect": False
                }
    Logger.Log(f"Unusual turn of events during check the token", 3)
    raise HTTPException(status_code=500)

@app.get("/wishes", response_model=list[WishesDatabaseModel])
async def GetAllWishes(): 
    Logger.Log(f"Trying to get all wishes for user", 1)
    if(DatabaseFriend):
        try:
            return await DatabaseFriend.GetAllWishes()
        except DatabaseFriendGetWishesError:
            Logger.Log(f"Get all wishes failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't get all wishes. Database access error."
            )
    Logger.Log(f"Unusual turn of events during get all wishes", 3)
    raise HTTPException(status_code=500)

@app.get("/wishes/{WishID}", response_model=WishesDatabaseModel)
async def GetWishByID(WishID: int): 
    Logger.Log(f"Trying to get wish by ID", 1)
    if(DatabaseFriend):
        try:
            return await DatabaseFriend.GetWishByID(WishID)
        except DatabaseFriendWishNotFoundError:
            raise HTTPException(
                status_code=404, 
                detail=f"Wish with ID = {WishID} not found"
            )
        except DatabaseFriendGetWishesError:
            Logger.Log(f"Get wish by ID failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't get wish by ID. Database access error."
            )
    Logger.Log(f"Unusual turn of events during get wish by ID", 3)
    raise HTTPException(status_code=500)

@app.get("/{Login}/wishes", response_model=list[WishesDatabaseModel])
async def GetWishes(Login: str): 
    Logger.Log(f"Trying to get wishes for user {Login}", 1)
    if(DatabaseFriend):
        try:
            return await DatabaseFriend.GetWishes(Login)
        except DatabaseFriendGetWishesError:
            Logger.Log(f"Get wishes for user {Login} failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't get the wishes. Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            Logger.Log(f"Get wishes for user {Login} failed. User not found", 4)
            raise HTTPException(
                status_code=404, 
                detail="Can't get the wishes. User not found."
            )
    Logger.Log(f"Unusual turn of events during get the wishes", 3)
    raise HTTPException(status_code=500)

@app.post("/{Login}/wishes", response_model=WishIDModel)
async def CreateWishes(Login: str, Body: WishesRequestBodyModel): 
    Logger.Log(f"User {Login} trying to create wish", 1)
    if(DatabaseFriend):
        try:
            TokenCorrect = DatabaseFriend.CheckToken(Login, Body.Token)
        except DatabaseFriendCheckTokenError:
            Logger.Log(f"Check token of user {Login} failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't check token. Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            Logger.Log(f"Check token of user {Login} failed. User not found", 4)
            raise HTTPException(
                status_code=404, 
                detail="Can't check token. User not found."
            )
        else:
            if(TokenCorrect):
                try:
                    return {
                        "ID": await DatabaseFriend.CreateWish(Login, Body)
                    }
                except DatabaseFriendCreateWishError:
                    Logger.Log(f"Create wish for user {Login} failed."\
                                                " Database access error", 4)
                    raise HTTPException(
                        status_code=500, 
                        detail="Can't create wish. Database access error."
                    )
            else:
                Logger.Log(f"Token of user {Login} incorrect. Access denied", 3)
                raise HTTPException(
                    status_code=401, 
                    detail="Token incorrect. Access denied."
                )
    Logger.Log(f"Unusual turn of events during create the wish", 3)
    raise HTTPException(status_code=500)

@app.put("/{Login}/wishes/{WishID}", response_model=None)
async def ChangeWishes(Login: str,  WishID: int, Body: WishesRequestBodyModel): 
    Logger.Log(f"User {Login} trying to update wish {WishID}", 1)
    if(DatabaseFriend):
        try:
            TokenCorrect = DatabaseFriend.CheckToken(Login, Body.Token)
        except DatabaseFriendCheckTokenError:
            Logger.Log(f"Check token of user {Login} failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't check token. Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            Logger.Log(f"Check token of user {Login} failed. User not found", 4)
            raise HTTPException(
                status_code=404, 
                detail="Can't check token. User not found."
            )
        else:
            if(TokenCorrect):
                try:
                    return await DatabaseFriend.UpdateWish(WishID, Body)
                except DatabaseFriendCreateWishError:
                    Logger.Log(f"Update wish for user {Login} failed."\
                                                " Database access error", 4)
                    raise HTTPException(
                        status_code=500, 
                        detail="Can't update wish. Database access error."
                    )
            else:
                Logger.Log(f"Token of user {Login} incorrect. Access denied", 3)
                raise HTTPException(
                    status_code=401, 
                    detail="Token incorrect. Access denied."
                )
    Logger.Log(f"Unusual turn of events during update the wish", 3)
    raise HTTPException(status_code=500)

@app.delete("/{Login}/wishes/{WishID}", response_model=None)
async def DeleteWishes(Login: str, WishID: int, Body: TokenRequestBodyModel):
    Logger.Log(f"User {Login} trying to delete wish {WishID}", 1)
    if(DatabaseFriend):
        try:
            TokenCorrect = DatabaseFriend.CheckToken(Login, Body.Token)
        except DatabaseFriendCheckTokenError:
            Logger.Log(f"Check token of user {Login} failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't check token. Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            Logger.Log(f"Check token of user {Login} failed. User not found", 4)
            raise HTTPException(
                status_code=404, 
                detail="Can't check token. User not found."
            )
        else:
            if(TokenCorrect):
                try:
                    Wish = await DatabaseFriend.GetWishByID(WishID)
                    User = await DatabaseFriend.GetUserWithoutPasswordByLogin(Login)
                    if(Wish and Wish["Owner"] == User["ID"]):
                        try:
                            return await DatabaseFriend.DeleteWish(WishID)
                        except DatabaseFriendCreateWishError:
                            Logger.Log(f"Delete wish for user {Login} failed."\
                                                        " Database access error", 4)
                            raise HTTPException(
                                status_code=500, 
                                detail="Can't delete wish. Database access error."
                            )
                    else:
                        Logger.Log(f"Delete wish with ID = {WishID} failed - access denied")
                        raise HTTPException(
                            status_code=403, 
                            detail=f"Can't delete wish. Access denied. You aren't the owner."
                        )
                except DatabaseFriendWishNotFoundError:
                    Logger.Log(f"Delete wish with ID = {WishID} failed - wish now found")
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Can't delete wish. Wish with ID = {WishID} not found."
                    )
                except (DatabaseFriendGetUserByLoginError, DatabaseFriendUserNotFoundError):
                    Logger.Log(f"Delete wish with ID = {WishID} failed - can't check owner")
                    raise HTTPException(
                        status_code=500, 
                        detail=f"Can't delete wish. Error while owner checking"
                    )
                except HTTPException as e:
                    raise e
                except:
                    raise HTTPException(status_code=500)

            else:
                Logger.Log(f"Token of user {Login} incorrect. Access denied", 3)
                raise HTTPException(
                    status_code=401, 
                    detail="Token incorrect. Access denied."
                )
    Logger.Log(f"Unusual turn of events during delete the wish", 3)
    raise HTTPException(status_code=500)




@app.get("/{Login}", response_model=UserInDatabaseWithoutPasswordModel)
async def GetUserInfo(Login: str):
    Logger.Log(f"Trying to get user info for login {Login}", 1)
    if(DatabaseFriend):
        try:
            return await DatabaseFriend.GetUserWithoutPasswordByLogin(Login)
        except DatabaseFriendGetWishesError:
            Logger.Log(f"Get get user info for login {Login} failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't get user info. Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            Logger.Log(f"Get get user info for login {Login} failed. User not found", 4)
            raise HTTPException(
                status_code=404, 
                detail="Can't get user info. User not found."
            )
    Logger.Log(f"Unusual turn of events during get user info", 3)
    raise HTTPException(status_code=500)

@app.put("/{Login}")
async def UpdateUserInfo(Login: str, Body: UserRequestBodyModel):
    Logger.Log(f"Trying to update {Login} user info", 1)
    if(DatabaseFriend):
        try:
            TokenCorrect = DatabaseFriend.CheckToken(Login, Body.Token)
        except DatabaseFriendCheckTokenError:
            Logger.Log(f"Check token of user {Login} failed. Database error", 4)
            raise HTTPException(
                status_code=500, 
                detail="Can't check token. Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            Logger.Log(f"Check token of user {Login} failed. User not found", 4)
            raise HTTPException(
                status_code=404, 
                detail="Can't check token. User not found."
            )
        else:
            if(TokenCorrect):
                try:
                    return await DatabaseFriend.UpdateUserInfoByLogin(Login, Body)
                except DatabaseFriendUpdateUserByLoginError:
                    Logger.Log(f"Can't update user info. Database error")
                    raise HTTPException(
                        status_code=500, 
                        detail="Can't update user info. Database error."
                    )
            else:
                Logger.Log(f"Token of user {Login} incorrect. Access denied", 3)
                raise HTTPException(
                    status_code=401, 
                    detail="Token incorrect. Access denied."
                )
    Logger.Log(f"Unusual turn of events during delete the wish", 3)
    raise HTTPException(status_code=500)