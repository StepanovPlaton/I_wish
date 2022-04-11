from imp import reload
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from utils.Logger import LoggerClass
from utils.ConfigReader import ConfigClass
from utils.YAMLReader import YAMLReaderClass

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="debug", log_config="config.yaml", reload=True)
    quit()

YAMLReader = YAMLReaderClass()
Config = ConfigClass(YAMLReader)
Logger = LoggerClass(Config)

class User(BaseModel):
    Login: str
    Password: str

app = FastAPI()

@app.on_event("startup") #type: ignore
async def startup():
    print("Server startup")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/auth")
async def auth(UserInfo: User):
    return {"Login": UserInfo.Login, "Password": UserInfo.Password}

