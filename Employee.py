""" Informacoes dos funcionarios, para login remoto """
from models.Models import db, MEmployee, MEmployeeTime
from sqlalchemy import and_
import datetime

class Employee(object):
    def __init__(self, username, pwd_hash):
        self.ID = False
        self.username = username
        self.pwd_hash = pwd_hash
        self._muser = None

    def insertIntoDatabase(self):
        self._muser = MEmployee(self.username, self.pwd_hash, None)
        db.session.add(self._muser)
        db.session.commit()
        self.ID = self._muser.id
        return self.ID

    def removeFromDatabase(self):
        db.session.delete(self._muser)
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

    def getEmployeeTime(self, months=1):
        """ Retrieve an array containing the time records for last 'months'
        months """
        datecurrent = datetime.datetime.now()
        
        mtimes = MEmployeeTime.query.filter(MEmployeeTime.employee_id==self.ID)
        mtimes_list = []

        for mtime in mtimes:
            mtimes_list.append({'login':str(mtime.employee_time_login),
                                'logout':str(mtime.employee_time_logout)})

        return mtimes_list

    @staticmethod
    def getUserByID(userid):
        muser = MEmployee.query.get(userid)
        if muser is None:
            return False

        emp = Employee(muser.employee_login, muser.employee_pwd_hash)
        emp.ID = muser.id
        emp._muser = muser
        return emp        

    @staticmethod
    def getUserByUsername(username):
        muser = MEmployee.query.filter_by(employee_login=username).first()

        if muser is None:
            return False

        memp = Employee(muser.employee_login, muser.employee_pwd_hash)
        memp.ID = muser.id
        memp._muser = muser
        return memp

    
        
