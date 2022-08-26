from pathlib import Path

from utils.YAMLReader import *

class ConfigError(Exception): pass
class ConfigNotFound(ConfigError, FileNotFoundError): pass

import os
from dotenv import load_dotenv
from functools import reduce

class ConfigClass():
    def __init__(self, YAMLReader: YAMLReaderClass, PathToConfig: str ="../config.yaml", quiet: bool =False) -> None: 
        try:
            self.Config = YAMLReader.ReadYamlFile(PathToConfig)
        except Exception:
            raise ConfigNotFound("Error while reading config.yaml")

        self.Config["ParserRootPath"] = Path(__file__).parents[1]

        if (self.Config["ParserRootPath"] / '.env').exists():
            load_dotenv(self.Config["ParserRootPath"] / '.env')

        

        if(not "Database" in self.Config.keys()):
            EnvironmentDatabaseVariables = [
                "IWISH_SERVER_HOST", 
                "IWISH_SERVER_PORT", 
                "IWISH_SERVER_USER", 
                "IWISH_SERVER_PASSWORD", 
                "IWISH_SERVER_DATABASE"
            ]
            if(
                reduce(
                    lambda AllFound, Current:
                        AllFound if Current in os.environ.keys() else False, 
                    EnvironmentDatabaseVariables, 
                    True
                )
            ):
                self.Config["Database"] = {}
                self.Config["Database"]["host"] = os.environ.get("IWISH_SERVER_HOST")
                self.Config["Database"]["port"] = os.environ.get("IWISH_SERVER_PORT")
                self.Config["Database"]["user"] = os.environ.get("IWISH_SERVER_USER")
                self.Config["Database"]["password"] = os.environ.get("IWISH_SERVER_PASSWORD")
                self.Config["Database"]["database"] = os.environ.get("IWISH_SERVER_DATABASE")
            else: 
                raise ConfigError(".env file not full")

        if(not quiet): print("Config attach")
