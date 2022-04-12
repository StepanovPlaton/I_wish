import psycopg2

from utils.Logger import LoggerClass
from utils.ConfigReader import ConfigClass, ConfigError

class DatabaseFriendError(Exception): pass
class DatabaseConnectionDataNotFound(DatabaseFriendError, ConfigError): pass

class DatabaseFriendClass:
    def __init__(self, Config: ConfigClass, Logger: LoggerClass):
        self.Config = Config.Config
        self.Logger = Logger

        self.Connection: psycopg2.connection | None = None
        self.DatabaseCursor: psycopg2.cursor | None = None

        self.Logger.Log("Initialization (DatabaseFriend) module...", 1)
        self.Logger.Log("Try read database authorization data from config.yaml", 1)
        try:
            self.AuthorizationData: dict[str, str] = self.Config["Database"]
            _ = self.Config["Database"]["host"]
            _ = self.Config["Database"]["port"]
            _ = self.Config["Database"]["user"]
            _ = self.Config["Database"]["password"]
            _ = self.Config["Database"]["database"]
        except:
            self.Logger.Log("Can't read data for connection to database from config.yaml", 5)
            raise DatabaseConnectionDataNotFound()
        else:
            self.Logger.Log("Read database authorization data - OK", 1)
            self.Logger.Log(f"Try connection to database ({self.AuthorizationData['host']}:"\
                                f"{self.AuthorizationData['port']}/{self.AuthorizationData['database']})")
            try:
                self.Connection = psycopg2.connect(**self.AuthorizationData) #type: ignore
                self.DatabaseCursor = self.Connection.cursor() #type: ignore
            except BaseException as e:
                self.Logger.Log("Failed to connection to database!", 5)
                self.Logger.Log(str(e), 5)
                raise
            else: self.Logger.Log("Connection to database - success")
        self.Logger.Log("(DatabaseFriend) module ready to work", 1)