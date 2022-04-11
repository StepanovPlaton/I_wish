from typing import Any
import logging

from utils.ConfigReader import ConfigClass

class LoggerError(Exception): pass
class UnknownLogLevel(LoggerError, ValueError): pass
class NotSetLogLevel(LoggerError, ValueError): pass

class LoggerClass():
    def __init__(self, Config: ConfigClass):
        self.Config = Config.Config
        self.Levels = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        self.NeedIndent = False

        try: self.CurrentLevel: str = self.Config['Log']['Level']
        except Exception: 
            self.Log("Error while loading logging system. Log level not set in config.yaml", "CRITICAL")
            raise NotSetLogLevel()

        if(self.CurrentLevel not in self.Levels):
            self.Log("Error while loading logging system. Unknown log level", "CRITICAL")
            raise UnknownLogLevel()


        try: self.Colorise: bool = self.Config['Log']['Colorise']
        except Exception: 
            self.Log("Not found color flag in config.yaml. Colorise output disabled", "WARNING")
            self.Colorise = False

        logging.basicConfig(level=(self.Levels.index(self.CurrentLevel)+1)*10, filename="./main.log", filemode="w", format='{App}     [%(asctime)s]\t (%(levelname)s): %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        self.Log("Logger start")


    def LevelForLogging(self, Level: str) -> int: 
        LevelIndex = self.Levels.index(Level)
        if(LevelIndex != -1): return (LevelIndex+1)*10
        else: raise UnknownLogLevel()


    def Log(self, Message: str, Level: str | int ="INFO") -> None:
        if(isinstance(Level, str) and (Level not in self.Levels)): self.Log(Message, Level="INFO")
        if(isinstance(Level, int)):
            if(Level < 0 or Level > len(self.Levels)): self.Log(Message, Level="INFO")
            else: self.Log(Message, Level=self.Levels[Level])

        # Level next type only 'str'
        if(isinstance(Level, str) and self.Levels.index(Level) < self.Levels.index(self.CurrentLevel)): return

        if(self.Colorise): 
            if(Level == "DEBUG"): print(f"{LogColors.OkBlue}", end="")
            if(Level == "INFO"): print(f"{LogColors.Bold}", end="")
            if(Level == "WARNING"): print(f"{LogColors.Warning}", end="")
            if(Level == "ERROR"): print(f"{LogColors.Error}", end="")
            if(Level == "CRITICAL"): print(f"{LogColors.Broke}", end="")
        else: print(f"({self.CurrentLevel}): ")

        print(f"{Message}")
        logging.log(self.LevelForLogging(self.CurrentLevel), Message)

        if(self.Colorise): print(f"{LogColors.End}")

        if(Level != "DEBUG"): self.NeedIndent = True

    def DebugPrint(self, *Messages: Any):
        if(self.Colorise): print(f"{LogColors.OkBlue}")
        print(f"{' '.join([str(i) for i in Messages])}")
        if(self.Colorise): print(f"{LogColors.End}")

    def Indent(self): 
        if(self.NeedIndent): 
            print() 
            self.NeedIndent = False
    def Detach(self): 
        if(self.NeedIndent): 
            print(f"\n--- --- --- --- ---\n")
            self.NeedIndent = False

class LogColors: #
    Header = '\033[95m'
    
    OkBlue = '\033[94m'
    OkCyan = '\033[96m'
    OkGreen = '\033[92m'
    
    Warning = '\033[93m'
    Error = '\033[91m'
    Broke = '\033[91m\033[1m\033[4m'
    
    End = '\033[0m'

    Bold = '\033[1m'
    Underline = '\033[4m'