import os
import psutil
import pyperclip


class SystemUtils:
    @staticmethod
    def getEnv(key: str = None):
        """ get environment variables """
        if key is None:
            return os.environ
        else:
            try:
                return os.environ[key]
            except KeyError:
                return None

    @staticmethod
    def bytesToGb(size, number=2):
        return f"{size / (1024 ** 3):.{number}f}GB"

    @staticmethod
    def getCupCount(logical=True):
        """ get cup count """
        return psutil.cpu_count(logical)

    @staticmethod
    def getMemoryUsedPercent():
        """ get memory percent """
        return f"{psutil.virtual_memory().percent}%"

    @staticmethod
    def getCpuPercent(interval=1.0):
        """ get cpu percent """
        return f"{psutil.cpu_percent(interval)}%"

    @staticmethod
    def getPasteContent():
        """ get paste content """
        return pyperclip.paste()

    def copyContentToPaste(self, string):
        """ copy content to paste """
        pyperclip.copy(string)
        return self

    def disableUser(self, userName):
        """ disable user """
        os.system(f'net user {userName} /active:no')
        return self

    def enableUser(self, userName):
        """ enable user"""
        os.system(f'net user {userName} /active:yes')
        return self

    def createUser(self, userName, password, isManager=False):
        """ create system user"""
        if isManager:
            os.system(f'net user {userName} {password} /add')
            os.system(f'net localgroup Administrators {userName} /add')
        else:
            os.system(f'net user {userName} {password} /add')
        return self

    def removeUser(self, userName):
        """ remove system user """
        os.system(f'net user {userName} /del')
        return self

    def execSystemCommand(self, command: str):
        """ execute system command """
        os.system(command)
        return self

    def execSystemCommands(self, commands: list[str]):
        """ execute system commands """
        for command in commands:
            os.system(command)
        return self

    def getMemorySize(self, isGB=False, number=2):
        """ get memory size """
        size = psutil.virtual_memory().total
        if isGB:
            return self.bytesToGb(size, number)
        else:
            return size

    def getMemoryUsed(self, isGB=False, number=2):
        """ get memory used size """
        size = psutil.virtual_memory().used
        if isGB:
            return self.bytesToGb(size, number)
        else:
            return f"{size}byte"

    def getDiskSize(self, path: str, isGB=False, number=2):
        """ get disk size """
        size = psutil.disk_usage(path).total
        if isGB:
            return self.bytesToGb(size, number)
        else:
            return f"{size}byte"


