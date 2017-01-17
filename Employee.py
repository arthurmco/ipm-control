""" Informações dos funcionários, para login remoto """

class Employee(object):
    def __init__(self, username, pwd_hash):
        self.ID = False
        self.username = username
        self.pwd_hash = pwd_hash

    def insertIntoDatabase(self):
        pass

    def removeFromDatabase(self):
        pass

    def checkPassword(self, pwd_hash):
        """ Checks password.
        Checks if the employee password hash and 'pwd_hash' are the same.
        If not, then return False. If yes, return True """
        pass

    def registerEmployeeTime(self, login_time, logout_time):
        """ Register employee login and logout time, for conference """

    @staticmethod
    def getUserByID(userid):
        pass

    @staticmethod
    def getUserByUsername(username):
        pass

    
        
