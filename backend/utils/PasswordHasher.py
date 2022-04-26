from passlib.context import CryptContext

class PasswordHasherClass:
    def __init__(self):
        self.Hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def HashOfPassword(self, Password: str) -> str:
        return self.Hasher.hash(Password) #type: ignore

    def CheckPassword(self, Hash: str, Password: str) -> bool:
        return self.Hasher.verify(Password, Hash) #type: ignore