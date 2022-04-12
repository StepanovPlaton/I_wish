#!/usr/bin/python

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn #type: ignore

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0]))

from utils.YAMLReader import YAMLReaderClass
from utils.ConfigReader import ConfigClass
from utils.Logger import LoggerClass
from utils.DatabaseFriend import DatabaseFriendClass

YAMLReader = YAMLReaderClass()
Config = ConfigClass(YAMLReader)
Logger = LoggerClass(Config)
DatabaseFriend: DatabaseFriendClass | None = None

class User(BaseModel):
    Login: str
    Password: str

app = FastAPI()

@app.on_event("startup") #type: ignore
async def startup():
    global DatabaseFriend

    Logger.Log("Server startup - OK", 2)
    DatabaseFriend = DatabaseFriendClass(Config, Logger)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/auth")
async def auth(UserInfo: User):
    return {"Login": UserInfo.Login, "Password": UserInfo.Password}

