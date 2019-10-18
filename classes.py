class Session:
    def __init__(self, uid, sessionType, timeSignedIn):
        self.uid = uid
        self.sesionType = sessionType
        self.timeSignedIn = timeSignedIn

    def login(self, username, password, sType):
        # If username + password matches record in db
        # return true else false
        if username:  # (pseudo) need to verify if user details match
            self.sessionType = sType
            return True
        else:
            return False

    def logout(self):
        self.uid = None
        self.sessionType = None
        self.timeSignedIn = None


class Account:
    def __init__(self, accountNumber, accountName, balance):
        self.accountNumber = accountNumber
        self.accountName = accountName
        self.balance = balance

    def setAccountNumber(self, accNumber):
        self.accountNumber = accNumber

    def setAccountName(self, accName):
        self.accountName = accName

    def setBalance(self, bal):
        self.balance = bal
