""" Database singleton class """

from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy

class Database(object):
    """ This will encapsulate the SQLAlchemy database class in an object.
    So I can use this and don't have to use the app object all time """
    def __init__(self, app):
        self.db = SQLAlchemy(app)
        

    @staticmethod
    def createDatabase(app):
        Database.database = Database(app)
        from Models import *
        return Database.database

        

Database.database = None

def installDatabase(db):
    """ Install the database into the server.
    Creates all tables """
    db.create_all()
