import asyncpg

from utils.Logger import LoggerClass
from utils.ConfigReader import ConfigClass, ConfigError
from utils.Models import *
from utils.Hasher import HasherClass

class DatabaseConnectorError(Exception): pass
class DatabaseConnectionDataNotFound(DatabaseConnectorError, ConfigError): pass
class DatabaseConnectionFailed(DatabaseConnectorError): pass
class DatabaseTransactionFailed(DatabaseConnectorError): pass

class DatabaseConnectorClass:
    def __init__(self, Config: ConfigClass, Logger: LoggerClass, \
                    Hasher: HasherClass):
        self.Config = Config.Config
        self.Logger = Logger
        self.Hasher = Hasher

        self.Connection: asyncpg.Connection[asyncpg.Record] | None = None
        self.ConnectionChecked: bool = False

        self.Logger.Log("Initialization (DatabaseConnector) module...", 1)
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

    async def CheckDatabaseConnection(self) -> bool:
        self.Logger.Log("Read database authorization data - OK", 1)
        self.Logger.Log(f"Try connection to database ({self.AuthorizationData['host']}:"\
                f"{self.AuthorizationData['port']}/{self.AuthorizationData['database']})")
        try:
            self.Connection = await asyncpg.connect(**self.AuthorizationData)
        except BaseException as e:
            self.Logger.Log("Failed to connection to database!", 5)
            self.Logger.Log(f"asyncpg return exception - {e}", 5)
            raise DatabaseConnectionFailed()
        else: 
            self.ServerVersion = self.Connection.get_server_version()
            self.ServerPID = self.Connection.get_server_pid()
            await self.Connection.close()
            self.Logger.Log("Connection to database - success. "\
                f"Server version - {self.ServerVersion.releaselevel}."\
                    f"{self.ServerVersion.major}.{self.ServerVersion.minor}."\
                    f"{self.ServerVersion.micro}, pid - {self.ServerPID}")
            self.ConnectionChecked = True
        self.Logger.Log("(DatabaseConnector) module ready to work", 1)
        return True

    async def Request(self, Request: str): 
        if(not self.ConnectionChecked):
            self.Logger.Log("Connection to database not checked. Needed check "\
                "connection before execute request", 3)
            if(not await self.CheckDatabaseConnection()):
                raise DatabaseConnectionFailed()
        DatabaseConnection = await asyncpg.connect(**self.AuthorizationData,)
        try:
            self.Logger.Log(f"Send SQL request - {Request}", 1)
            return await DatabaseConnection.fetch(Request)
        except Exception as e:
            self.Logger.Log(f"SQL request crashed with error - {e}", 4)
            await DatabaseConnection.close()
            raise DatabaseTransactionFailed()


class DatabaseFriendError(Exception): pass
class DatabaseFriendUserNotFoundError(DatabaseFriendError): pass

class DatabaseFriendCheckAuthorizationDataError(DatabaseFriendError): pass
class DatabaseFriendCheckLoginIsFreeError(DatabaseFriendError): pass
class DatabaseFriendRegistationNewUserError(DatabaseFriendError): pass
class DatabaseFriendCheckTokenError(DatabaseFriendError): pass
class DatabaseFriendGetWishesError(DatabaseFriendError): pass
class DatabaseFriendCreateWishError(DatabaseFriendError): pass
class DatabaseFriendUpdateWishError(DatabaseFriendError): pass
class DatabaseFriendDeleteWishError(DatabaseFriendError): pass

class DatabaseFriendClass(DatabaseConnectorClass):
    # SELECT * FROM public."Users" WHERE "Login" = '{Login}'
    GetUserByLoginRequest = "SELECT * FROM public.\"Users\" WHERE \"Login\" = '{Login}'"

    # INSERT INTO public."Users"("Login", "HashOfPassword") 
    #                               VALUES ('{Login}', '{HashOfPassword}');
    AddUserRequest = "INSERT INTO public.\"Users\"(\"Login\", \"HashOfPassword\")"\
	                    "VALUES ('{Login}', '{HashOfPassword}');"

    # SELECT "ID", "Wish", "Owner" FROM public."Wishes"
    # WHERE "Target" IN NULL AND 
    # "Owner" = (SELECT "ID" FROM public."Users" WHERE "Login" = '{Login}');
    GetWishesRequest = "SELECT \"ID\", \"Wish\", \"Owner\" FROM public.\"Wishes\""\
                        "WHERE \"Target\" IS NULL AND \"Owner\" = "\
                        "(SELECT \"ID\" FROM public.\"Users\" WHERE \"Login\" = '{Login}');"

    # INSERT INTO public."Wishes"("Wish", "Owner", "Target") 
    # VALUES ('{Wish}', (SELECT "ID" FROM public."Users" WHERE "Login" = '{Login}'), '{Target}')
    # RETURNING "ID";
    CreateWishRequest = "INSERT INTO public.\"Wishes\"(\"Wish\", \"Owner\", \"Target\")"\
                        "VALUES ('{Wish}', "\
                        "(SELECT \"ID\" FROM public.\"Users\" WHERE \"Login\" = '{Login}'),"\
                        " '{Target}') "\
                        "RETURNING \"ID\";"

    # INSERT INTO public."Wishes"("Wish", "Owner") 
    # VALUES ('{Wish}', (SELECT "ID" FROM public."Users" WHERE "Login" = '{Login}'))
    # RETURNING "ID";
    CreateWishWithoutTargetRequest = "INSERT INTO public.\"Wishes\"(\"Wish\", \"Owner\")"\
                        "VALUES ('{Wish}', "\
                        "(SELECT \"ID\" FROM public.\"Users\" WHERE \"Login\" = '{Login}')) "\
                        "RETURNING \"ID\";"

    # UPDATE public."Wishes" SET "Wish" = '{Wish}', "Owner" = {Owner}, 
    # "Target" = {Target} WHERE "ID" = {ID};
    UpdateWishRequest = "UPDATE public.\"Wishes\" SET \"Wish\" = '{Wish}', "\
                        "\"Owner\" = (SELECT \"ID\" FROM public.\"Users\" "\
                        "WHERE \"Login\" = '{Login}'), \"Target\" = {Target} WHERE \"ID\" = {ID};"

    # UPDATE public."Wishes" SET "Wish" = '{Wish}', "Owner" = {Owner} WHERE "ID" = {ID};
    UpdateWishWithoutTargetRequest = "UPDATE public.\"Wishes\" SET \"Wish\" = '{Wish}', "\
                        "\"Owner\" = (SELECT \"ID\" FROM public.\"Users\" "\
                        "WHERE \"Login\" = '{Login}') WHERE \"ID\" = {ID};"

    # DELETE FROM public."Wishes" WHERE "ID" = {ID} AND
    # and "Owner" = (SELECT "ID" FROM public."Users" WHERE "Login" = 'Test');
    DeleteWishRequest = "DELETE FROM public.\"Wishes\" WHERE \"ID\" = {ID} AND"\
            " \"Owner\" = (SELECT \"ID\" FROM public.\"Users\" WHERE \"Login\" = '{Login}');"
    
    # ----- Users -----
    
    async def CheckUserAuthorizationData(self, Login: str, Password: str) -> bool:
        try:
            PSQLResult: list[UserInDatabaseModel] = \
                await self.Request(self.GetUserByLoginRequest.format(Login=Login)) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't check user authorization data - failed database request", 4)
            raise DatabaseFriendCheckAuthorizationDataError()
        else:
            if(PSQLResult): 
                if(len(PSQLResult) == 1): 
                    User = PSQLResult[0]
                    return self.Hasher.CheckPassword(User["HashOfPassword"], Password)
                else:
                    self.Logger.Log("Found 2 users with the same logins", 5)
            else:
                self.Logger.Log("Can't check user authorization data - user not found", 3)
                raise DatabaseFriendUserNotFoundError()
        return False

    async def CheckLoginIsFree(self, Login: str) -> bool:
        try:
            PSQLResult = await self.Request(self.GetUserByLoginRequest.format(Login=Login))
        except DatabaseConnectorError:
            self.Logger.Log("Can't check if login is free - failed database request", 4)
            raise DatabaseFriendCheckLoginIsFreeError()
        else:
            if(PSQLResult): 
                if(len(PSQLResult) == 0): return True
            else: return True
        return False

    async def RegistationNewUser(self, Login: str, Password: str) -> None:
        try:
            await self.Request(self.AddUserRequest.format(Login=Login,\
                        HashOfPassword=self.Hasher.HashOfPassword(Password)))
        except DatabaseConnectorError:
            self.Logger.Log("Can't add new user - failed database request", 4)
            raise DatabaseFriendRegistationNewUserError()

    async def CheckToken(self, Login: str, Token: str) -> bool:
        try:
            PSQLResult: list[UserInDatabaseModel] = \
                await self.Request(self.GetUserByLoginRequest.format(Login=Login)) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log(f"Can't check token for user {Login} - failed database request", 4)
            raise DatabaseFriendCheckTokenError()
        else:
            if(PSQLResult and len(PSQLResult)>0): 
                User = PSQLResult[0]
                return self.Hasher.CheckToken(Token, Login, User["HashOfPassword"])
            else:
                self.Logger.Log(f"Can't check token for user {Login} - user not found", 3)
                raise DatabaseFriendUserNotFoundError()


    # ----- Wishes -----

    async def GetWishes(self, Login: str) -> list[WishesWithoutTargetDatabaseModel]:
        try:
            PSQLResult: list[WishesWithoutTargetDatabaseModel] = \
                    await self.Request(self.GetWishesRequest.format(Login=Login)) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't get the wishes - failed database request", 4)
            raise DatabaseFriendGetWishesError()
        else:
            if(PSQLResult): return PSQLResult
            else:
                self.Logger.Log(f"List wishes for user {Login} empty", 3)
                return PSQLResult
        
    async def CreateWish(self, Login: str, Wish: WishesRequestBodyModel) -> int:
        try:
            if(Wish.Target):
                return (await self.Request(self.CreateWishRequest.format(\
                                            Login=Login, **vars(Wish))))[0]["ID"] #type: ignore
            else:
                return (await self.Request(self.CreateWishWithoutTargetRequest.format(\
                                            Login=Login, **vars(Wish))))[0]["ID"] #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't create wish - failed database request", 4)
            raise DatabaseFriendCreateWishError()

    async def UpdateWish(self, Login: str, WishID: int, Wish: WishesRequestBodyModel) -> None:
        #TODO: Wish ID not found!
        try:
            if(Wish.Target):
                await self.Request(self.UpdateWishRequest.format(Login=Login, ID=WishID, \
                                                **vars(Wish))) #type: ignore
            else:
                await self.Request(self.UpdateWishWithoutTargetRequest.format(Login=Login, \
                                    ID=WishID, **vars(Wish))) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't update wish - failed database request", 4)
            raise DatabaseFriendUpdateWishError()

    async def DeleteWish(self, Login: str, WishID: int) -> None:
        #TODO: Wish ID not found!
        #TODO: Don't touch someone else's
        try:
            await self.Request(self.DeleteWishRequest.format(\
                                            Login=Login, ID=WishID)) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't delete wish - failed database request", 4)
            raise DatabaseFriendDeleteWishError()