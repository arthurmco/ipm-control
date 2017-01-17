""" Database singleton class """

from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy

class Database(object):
    """ This will encapsulate the SQLAlchemy database class in an object.
    So I can use this and don't have to use the app object all time """
    def __init__(self, app=None):
        self.db = SQLAlchemy(app)
        

        
    @staticmethod
    def createDatabase(app):
        Database.database = Database(app)

        import Models
        Database.database.db.create_all()        
        
        return Database.database


Database.database = Database()
