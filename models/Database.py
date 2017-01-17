""" Database singleton class """

from flask_sqlalchemy import SQLAlchemy

class Database(object):
    """ This will encapsulate the SQLAlchemy database class in an object.
    So I can use this and don't have to use the app object all time """
    def __init__(self, app):
        self.db = SQLAlchemy(app)

    database=False
    
    @staticmethod
    def createDatabase(app):
        Database.database = Database(app)
        return Database.database
