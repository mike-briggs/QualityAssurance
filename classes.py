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
