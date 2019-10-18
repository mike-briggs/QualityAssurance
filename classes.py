class user:
	def __init__(self, username, password, fname, lname):
		self.username = username
		self.password = password
		self.fname	  = fname
		self.lname	  = lname
	
	def getUser(self):
		print(self.fname+" "+self.lname);
		