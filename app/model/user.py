import app.utils as utils
from app.model.account import Account

class User:
    
    def __init__(self, username):
        self.username = username
        self.accountList = []

    def setPassword(self, password):
        self.passKey = password

    def getPassword(self):
        return self.passKey

    def getUsername(self):
        return self.username
    
    def matchPassword(self, pwd):
        userData = utils.openData("User")
        if self.username in userData:
            try:
                keyword = utils.decrypt(userData[self.username], pwd, True)
                if pwd == keyword:
                    self.setPassword(keyword)
                    userData.close()
                    return True
            except:
                msg = 'Username and password doesn\'t match'
        userData.close()
        return False

    def changePassword(self, newPassword):
        userData = utils.openData("User")        
        
        #change all accounts in the shelf file
        accountData = utils.openData(self.username)
        for key in accountData:
            pwd = utils.decrypt(accountData[key], self.getPassword())
            accountData[key] = utils.encrypt(pwd, newPassword)
        accountData.close()

        userData[self.username] = utils.encrypt(newPassword, newPassword, True)
        self.setPassword(newPassword)
        userData.close()

    def addAccount(self, account, newPassword):
        data = utils.openData(self.getUsername())
        account.setAccountPassword(utils.encrypt(newPassword, self.getPassword()))
        data[account.getKey()] = account.getAccountPassword();
        data.close()
        self.accountList.append(account)

    def isExisting(self):
        userData = utils.openData("User")
        exist = self.username in userData
        userData.close()
        return exist

    def isAccountExist(self, account):
        data = utils.openData(self.getUsername())
        key = account.getKey()
        exist = key in data
        data.close()
        return exist

    def getAccountList(self, force=False):
        if len(self.accountList) > 0 and not force:
            return self.accountList
        else:
            self.accountList.clear()
            accountData = utils.openData(self.username)
            for key in accountData:
                splitKey = key.split("_**_")
                account = Account(splitKey[0])
                account.setAccountUsername(splitKey[1])
                account.setAccountPassword(accountData[key])
                self.accountList.append(account)
            accountData.close()
            return self.accountList

    def removeAccount(self, account):
        data = utils.openData(self.getUsername())
        del data[account.getKey()]
        data.close()
        self.accountList.remove(account)
