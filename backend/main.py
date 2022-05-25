#!/usr/bin/python

from fastapi import FastAPI, HTTPException
import uvicorn #type: ignore

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0]))

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
    if(not await DatabaseFriend.CheckDatabaseConnection()):
        raise DatabaseConnectionFailed()

@app.get("/") 
async def root():
    return {"message": "Hello World"}

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
                return { 
                    "Token": Hasher.GetToken(Login, \
                                    Hasher.HashOfPassword(Password)) 
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
                    await DatabaseFriend.RegistationNewUser(Login, Password)
                except DatabaseFriendRegistationNewUserError:
                    Logger.Log(f"Registration with login ({Login}) failed "\
                                                    "Database error", 4)
                    raise HTTPException(
                        status_code=500, 
                        detail="Registration impossible. Database access error."
                    )
                else: 
                    return { 
                        "Token": Hasher.GetToken(Login, \
                                        Hasher.HashOfPassword(Password)) 
                    }
            else:
                Logger.Log(f"Login ({Login}) busy. Registation user impossible", 3)
                raise HTTPException(
                    status_code=409, 
                    detail="The selected username is already taken"
                )
    Logger.Log(f"Unusual turn of events during registration", 3)
    raise HTTPException(status_code=500)

@app.post("/check_token")
async def CheckToken(Login: str, Body: TokenRequestBodyModel):
    Logger.Log(f"User {Login} trying check token", 1)
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

@app.get("/{Login}/wishes", response_model=list[WishesWithoutTargetDatabaseModel])
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
                    return await DatabaseFriend.UpdateWish(Login, WishID, Body)
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

@app.delete("/{Login}/wishes/{WishID}")
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
                    return await DatabaseFriend.DeleteWish(Login, WishID)
                except DatabaseFriendCreateWishError:
                    Logger.Log(f"Delete wish for user {Login} failed."\
                                                " Database access error", 4)
                    raise HTTPException(
                        status_code=500, 
                        detail="Can't delete wish. Database access error."
                    )
            else:
                Logger.Log(f"Token of user {Login} incorrect. Access denied", 3)
                raise HTTPException(
                    status_code=401, 
                    detail="Token incorrect. Access denied."
                )
    Logger.Log(f"Unusual turn of events during delete the wish", 3)
    raise HTTPException(status_code=500)