class user:
    def __init__(self, userid, username, password, fname, lname):
        self.userid = userid
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname

    def getName(self):
        print(self.fname+" "+self.lname)

    def setName(self, first, last):
        self.fname = first
        self.lname = last

    def setUsername(self, un):
        self.username = un

    def getUsername(self):
        print(self.username)

    def setPassword(self, pw):
        self.password = pw


class session:
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
