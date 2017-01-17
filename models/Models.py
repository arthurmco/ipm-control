from Database import Database
""" Model interfaces for every database object here """

db = Database.database.db

class MClient(db.Model):
    """ Model interface for the client """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(80), unique=True)
    client_license_file = db.Column(db.String(255), unique=True)
    client_license_pub = db.Column(db.Binary(2048))
    client_license_pri = db.Column(db.Binary(2048))

    
    def __init__(self, name, license_file, license_pub, license_pri):
        self.client_name = name
        self.client_license_file = license_file
        self.client_license_pub = license_pub
        self.client_license_pri = license_pri

    def __repr__(self):
        return '<Client %r>' % self.client_name


class MHardware(db.Model):
    """ Model interface for the hardware """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer)
    hw_name = db.Column(db.String(96))
    hw_desc = db.Column(db.String(255))

    
    def __init__(self, client_id, name, desc):
        self.client_id = client_id
        self.hw_name = name
        self.hw_desc = desc

    def __repr__(self):
        return '<Hardware %r>' % self.hw_name
 
from datetime import datetime

class MEmployee(db.Model):
    """ Model interface for the employee """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_login = db.Column(db.String(48), unique=True)
    employee_pwd_hash = db.Column(db.String(256))
    employee_admission = db.Column(db.DateTime)
    employee_demission = db.Column(db.DateTime)

    def __init__(self, login, pwd_hash, admission, demission=None):
        self.employee_login = login
        self.employee_pwd_hash = pwd_hash
        self.employee_admission = admission
        if demission is None:
            demission = datetime.strptime('Dec 1 9999  9:99PM',
                                          '%b %d %Y %I:%M%p')

        self.employee_demission = demission

    def __repr__(self):
        return '<Employee %r>' % self.employee_login


class MEmployeeTime(db.Model):
    """ Model interface for the employee time registers """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer)
    employee_time_login = db.Column(db.DateTime)
    employee_time_logout = db.Column(db.DateTime)

    def __init__(self, employee_id, employee_login, employee_logout):
        self.employee_id = employee_id
        self.employee_time_login = employee_login
        self.employee_time_logout = employee_logout


    def __repr__(self):
        return '<Employee Time %r (%r %r)>' % self.employee_id, self.employee_time_login, self.employee_time_logout
