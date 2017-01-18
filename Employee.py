""" Informações dos funcionários, para login remoto """
from models.Models import db, MEmployee, MEmployeeTime

class Employee(object):
    def __init__(self, username, pwd_hash):
        self.ID = False
        self.username = username
        self.pwd_hash = pwd_hash
        self._mcli = None

    def insertIntoDatabase(self):
        self._mcli = MEmployee(self.username, self.pwd_hash, None)
        db.session.add(self._mcli)
        db.session.commit()
        self.ID = self._mcli.id
        return self.ID

    def removeFromDatabase(self):
        db.session.delete(self._mcli)
        db.session.commit()
        self.ID = False

    def checkPassword(self, pwd_hash):
        """ Checks password.
        Checks if the employee password hash and 'pwd_hash' are the same.
        If not, then return False. If yes, return True """
        if self.pwd_hash == pwd_hash:
            return True

        return False

    def registerEmployeeTime(self, login_time, logout_time):
        """ Register employee login and logout time, for conference """
        memptime = MEmployeeTime(self.ID, login_time, logout_time)
        db.session.add(memptime)
        db.session.commit()

    @staticmethod
    def getUserByID(userid):
        pass

    @staticmethod
    def getUserByUsername(username):
        muser = MEmployee.query.filter_by(employee_login=username).first()

        memp = Employee(muser.employee_login, muser.employee_pwd_hash)
        return memp

    
        
