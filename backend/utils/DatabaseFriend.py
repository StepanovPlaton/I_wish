from typing import Any
from databases import Database

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

        self.Database: Database | None = None
        self.ConnectionURL : str = "postgresql://{user}:{password}@{host}:{port}/{database}"
        self.DatabasesInited: bool = False

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

    async def DatabaseInit(self) -> bool:
        self.Logger.Log("Read database authorization data - OK", 1)
        self.Logger.Log(f"Try connection to database ({self.AuthorizationData['host']}:"\
                f"{self.AuthorizationData['port']}/{self.AuthorizationData['database']})")
        try:
            self.Database = Database(self.ConnectionURL.format(**self.AuthorizationData))
            await self.Database.connect()
        except BaseException as e:
            self.Logger.Log("Failed to connection to database!", 5)
            self.Logger.Log(f"asyncpg return exception - {e}", 5)
            raise DatabaseConnectionFailed()
        else: 
            self.DatabasesInited = True
            self.DatabaseVersion: str = (await self.Request("SELECT version();"))[0]["version"]
            #await self.Database.disconnect()
            self.Logger.Log("Connection to database - success. "\
                            f"Database version - {self.DatabaseVersion}")
        self.Logger.Log("(DatabaseConnector) module ready to work", 1)
        return True

    async def Request(self, Request: str, *args: dict[str, str | int], **other: str | int): 
        if(not self.DatabasesInited):
            self.Logger.Log("Database connection doesn't inited. Needed check "\
                "connection before execute request", 3)
            if(not await self.DatabaseInit()):
                raise DatabaseConnectionFailed()
        #self.Database = Database(self.ConnectionURL.format(**self.AuthorizationData))
        #await self.Database.connect()
        try:
            commonDict = {key: value for dict in [*args, other] for key, value in dict.items()}
            self.Logger.Log(f"Send SQL request - {Request} +{commonDict}", 1)
            DatabaseResponse: list[dict[str, Any]] = \
                list(map(lambda x: dict(x), await self.Database.fetch_all(Request, commonDict))) #type: ignore
            return DatabaseResponse
        except Exception as e:
            self.Logger.Log(f"SQL request crashed with error - {e}", 4)
            #await self.Database.disconnect()
            raise DatabaseTransactionFailed()



class DatabaseFriendError(Exception): pass
class DatabaseFriendUserNotFoundError(DatabaseFriendError): pass
class DatabaseFriendGetUserByLoginError(DatabaseFriendError): pass
class DatabaseFriendUpdateUserByLoginError(DatabaseFriendError): pass
class DatabaseFriendCheckAuthorizationDataError(DatabaseFriendError): pass
class DatabaseFriendCheckLoginIsFreeError(DatabaseFriendError): pass
class DatabaseFriendRegistrationNewUserError(DatabaseFriendError): pass
class DatabaseFriendCheckTokenError(DatabaseFriendError): pass
class DatabaseFriendGetWishesError(DatabaseFriendError): pass
class DatabaseFriendWishNotFoundError(DatabaseFriendError): pass
class DatabaseFriendCreateWishError(DatabaseFriendError): pass
class DatabaseFriendUpdateWishError(DatabaseFriendError): pass
class DatabaseFriendDeleteWishError(DatabaseFriendError): pass

class DatabaseFriendClass(DatabaseConnectorClass):
    # --- Users ---

    # SELECT * FROM public."Users" WHERE "Login" = '{Login}'
    GetUserByLoginRequest = 'SELECT * FROM public."Users" WHERE "Login"=:Login'

    # SELECT "ID", "Login", "Avatar" FROM public."Users" WHERE "Login" = '{Login}'
    GetUserWithoutPasswordByLoginRequest = 'SELECT "ID", "Login", "Avatar", "AboutMe", '\
                                '"Telegram" FROM public."Users" WHERE "Login" = :Login'

    # INSERT INTO public."Users"("Login", "HashOfPassword") 
    #                               VALUES ('{Login}', '{HashOfPassword}');
    AddUserRequest = 'INSERT INTO public."Users"("Login", "HashOfPassword")'\
                    'VALUES (:Login, :HashOfPassword);'

    # UPDATE public."Users"
	# SET "Avatar"=:Avatar, "AboutMe"=:AboutMe, "Telegram"=:Telegram
	# WHERE <condition>;
    UpdateUserInfoByLoginRequest = 'UPDATE public."Users" SET "Avatar"=:Avatar, '\
                '"AboutMe"=:AboutMe, "Telegram"=:Telegram WHERE "Login"=:Login;'

    # --- Wishes ---

    # SELECT public."Wishes"."ID", "Wish", public."Wishes"."Image", "Description", "Price", 
    # "Link", "Owner", "Login", public."Users"."Avatar"
    # FROM public."Wishes"
    # JOIN public."Users" ON public."Wishes"."Owner" = public."Users"."ID"
    # WHERE "Owner" = '1';
    GetWishesRequest = 'SELECT public."Wishes"."ID", "Wish", public."Wishes"."Image", '\
                        '"Description", "Price", "Link", "Anonymous", "HidingDate", "Owner", "Login", '\
                        'public."Users"."Avatar" FROM public."Wishes" JOIN public."Users"'\
                        ' ON public."Wishes"."Owner" = public."Users"."ID" WHERE "Login" = :Login;'

    # SELECT public."Wishes"."ID", "Wish", public."Wishes"."Image", "Description", "Price", 
    # "Link", "Owner", "Login", public."Users"."Avatar"
    # FROM public."Wishes"
    # JOIN public."Users" ON public."Wishes"."Owner" = public."Users"."ID";
    GetAllWishesRequest = 'SELECT public."Wishes"."ID", "Wish", public."Wishes"."Image", '\
                    '"Description", "Price", "Link", "Anonymous", "HidingDate", "Owner", '\
                    '"Login", public."Users"."Avatar" FROM public."Wishes" JOIN public.'\
                    '"Users" ON public."Wishes"."Owner" = public."Users"."ID";'

    # SELECT public."Wishes"."ID", "Wish", public."Wishes"."Image", "Description", "Price", 
    # "Link", "Owner", "Login", public."Users"."Avatar"
    # FROM public."Wishes"
    # JOIN public."Users" ON public."Wishes"."Owner" = public."Users"."ID"
    # WHERE public."Wishes"."ID" = 1;
    GetWishByIDRequest = 'SELECT public."Wishes"."ID", "Wish", public."Wishes"."Image",'\
                        ' "Description", "Price", "Link", "Anonymous", "HidingDate", '\
                        '"Owner", "Login", public."Users"."Avatar" FROM public."Wishes" '\
                        'JOIN public."Users" ON public."Wishes"."Owner" = public."Users".'\
                        '"ID" WHERE public."Wishes"."ID" = :WishID';

    # INSERT INTO public."Wishes"("Wish", "Owner", "Image", "Description", "Price", "Link")
    # VALUES ('{Wish}', (SELECT "ID" FROM public."Users" WHERE "Login" = '{Login}'), 
    # '{Image}', '{Description}', '{Price}', '{Link}')
    # RETURNING "ID";
    CreateWishRequest = 'INSERT INTO public."Wishes"("Wish", "Owner", "Image", "Description",'\
                        ' "Price", "Link", "Anonymous", "HidingDate") VALUES (:Wish, (SELECT "ID" FROM public."Users"'\
                        ' WHERE "Login" = :Login), :Image, :Description, '\
                        ':Price, :Link, :Anonymous, :HidingDate) RETURNING "ID";'

    # UPDATE public."Wishes"
	# SET "Wish"={Wish},  "Image"={Image}, "Description"={Description}, 
    # "Price"={Price}, "Link"={Link}
	# WHERE "ID"={ID};
    UpdateWishRequest = 'UPDATE public."Wishes" SET "Wish"=:Wish, '\
                        '"Image"=:Image, "Description"=:Description, "Price"=:Price, '\
                        '"Link"=:Link, "Anonymous"=:Anonymous, "HidingDate"=:HidingDate WHERE "ID"=:ID;'

    # DELETE FROM public."Wishes" WHERE "ID" = {ID};
    DeleteWishRequest = 'DELETE FROM public."Wishes" WHERE "ID" = :ID;'

    # ----- Users -----

    async def CheckUserAuthorizationData(self, Login: str, Password: str) -> bool:
        try:
            PSQLResult: list[UserInDatabaseModel] = \
                await self.Request(self.GetUserByLoginRequest, Login=Login) #type: ignore
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
            PSQLResult = await self.Request(self.GetUserByLoginRequest, Login=Login)
        except DatabaseConnectorError:
            self.Logger.Log("Can't check if login is free - failed database request", 4)
            raise DatabaseFriendCheckLoginIsFreeError()
        else:
            if(PSQLResult): 
                if(len(PSQLResult) == 0): return True
            else: return True
        return False

    async def RegistrationNewUser(self, Login: str, Password: str) -> None:
        try:
            await self.Request(self.AddUserRequest, Login=Login,\
                        HashOfPassword=self.Hasher.HashOfPassword(Password))
        except DatabaseConnectorError:
            self.Logger.Log("Can't add new user - failed database request", 4)
            raise DatabaseFriendRegistrationNewUserError()

    async def CheckToken(self, Login: str, Token: str) -> bool:
        try:
            PSQLResult: list[UserInDatabaseModel] = \
                await self.Request(self.GetUserByLoginRequest, Login=Login) #type: ignore
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

    async def GetUserWithoutPasswordByLogin(self, Login: str) -> UserInDatabaseWithoutPasswordModel:
        try:
            PSQLResult: list[UserInDatabaseWithoutPasswordModel] = \
                await self.Request(self.GetUserWithoutPasswordByLoginRequest, \
                                                        Login=Login) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't get user by login - failed database request", 4)
            raise DatabaseFriendGetUserByLoginError()
        else:
            if(PSQLResult): 
                if(len(PSQLResult) == 1): 
                    return PSQLResult[0]
                else:
                    self.Logger.Log("Found 2 users with the same logins", 5)
                    raise DatabaseFriendGetUserByLoginError()
            else:
                self.Logger.Log("Can't get user by login - user not found", 3)
                raise DatabaseFriendUserNotFoundError()

    async def UpdateUserInfoByLogin(self, Login: str, UserInfo: UserRequestBodyModel) -> None:
        try:
            await self.Request(self.UpdateUserInfoByLoginRequest, \
                    {key: value for key, value in vars(UserInfo).items() if key!='Token'}, \
                                        Login=Login) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't get user by login - failed database request", 4)
            raise DatabaseFriendUpdateUserByLoginError()

    # ----- Wishes -----

    async def GetWishes(self, Login: str) -> list[WishesDatabaseModel]:
        try:
            PSQLResult: list[WishesDatabaseModel] = \
                    await self.Request(self.GetWishesRequest, Login=Login) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't get the wishes - failed database request", 4)
            raise DatabaseFriendGetWishesError()
        else:
            if(PSQLResult): return PSQLResult
            else:
                self.Logger.Log(f"List wishes for user {Login} empty", 3)
                return PSQLResult

    async def GetWishByID(self, WishID: int) -> WishesDatabaseModel | None:
        try:
            PSQLResult: list[WishesDatabaseModel] = \
                    await self.Request(self.GetWishByIDRequest, \
                                                WishID=WishID) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't get the wish by ID - failed database request", 4)
            raise DatabaseFriendGetWishesError()
        else:
            if(PSQLResult): return PSQLResult[0]
            else: 
                self.Logger.Log("Requested wish ID does not exist", 4)
                raise DatabaseFriendWishNotFoundError()

    async def GetAllWishes(self) -> list[WishesDatabaseModel]:
        try:
            PSQLResult: list[WishesDatabaseModel] = \
                    await self.Request(self.GetAllWishesRequest) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't get all wishes - failed database request", 4)
            raise DatabaseFriendGetWishesError()
        else:
            if(PSQLResult): return PSQLResult
            else:
                self.Logger.Log(f"List with all wishes empty", 3)
                return PSQLResult
        
    async def CreateWish(self, Login: str, Wish: WishesRequestBodyModel) -> int:
        try:
            return (await self.Request(self.CreateWishRequest, \
                {key: value for key, value in vars(Wish).items() if key!='Token'}, \
                            Login=Login))[0]["ID"] #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't create wish - failed database request", 4)
            raise DatabaseFriendCreateWishError()

    async def UpdateWish(self, WishID: int, Wish: WishesRequestBodyModel) -> None:
        #TODO: Wish ID not found!
        try:
                await self.Request(self.UpdateWishRequest, \
                    {key: value for key, value in vars(Wish).items() if key!='Token'}, \
                    ID=WishID) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't update wish - failed database request", 4)
            raise DatabaseFriendUpdateWishError()

    async def DeleteWish(self, WishID: int) -> None:
        #TODO: Wish ID not found!
        #TODO: Don't touch someone else's
        try:
            await self.Request(self.DeleteWishRequest, ID=WishID) #type: ignore
        except DatabaseConnectorError:
            self.Logger.Log("Can't delete wish - failed database request", 4)
            raise DatabaseFriendDeleteWishError()
