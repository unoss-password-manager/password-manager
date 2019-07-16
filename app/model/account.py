import app.utils as utils
import pyperclip

class Account:
    
    def __init__(self, accountName):
        self.accountName = accountName

    def setAccountUsername(self, accountUsername):
        self.accountUsername = accountUsername

    def setAccountPassword(self, accountPassword):
        self.accountPassword = accountPassword

    def getAccountPassword(self):
        return self.accountPassword
        
    def getKey(self):
        return self.accountName + "_**_" + self.accountUsername

    def copyPassword(self, passKey):
        copas = utils.decrypt(self.accountPassword, passKey)
        pyperclip.copy(copas)
