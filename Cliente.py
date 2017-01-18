""" Dados sobre clientes e hardwares """

from models.Models import db, MClient
from sqlalchemy import or_

class Client(object):
    """ Define um cliente """
    def __init__(self, name):
        self.ID = False
        self.name = name
        self._mcli = None

    def addIntoDatabase(self):
        """ Adds into database. Returns client ID """
        self._mcli = MClient(self.name, self.name, '', '')
        db.session.add(self._mcli)
        db.session.commit()
        self.ID = self._mcli.id
        return self.ID

    def updateIntoDatabase(self):
        if self._mcli is None:
            return self.addIntoDatabase()

        self._mcli.client_name = self.name
        self._mcli.client_license_file = self.name + " license"
        db.session.add(self._mcli)
        db.session.commit()        

    def removeFromDatabase(self):
        """ Removes from database. Sets ID to false"""
        db.session.delete(self._mcli)
        db.session.commit()
        self.ID = False

    def getObjects(self):
        """ Retrieve a dictionary with safe objects. """
        return {'id': self.ID, 'name': self.name}

    def generateLicenseFile(self):
        """ Generate a license file, based on client ID 
        Fills the 'license_file' attribute with its path
        """
        pass

    def generateLicenseKey(self):
        """ Generate the license private and public keys 
        Fills the 'license_priv_key' and 'license_pub_key' attributes with them
        """
        pass

    @staticmethod
    def getClientFromID(client_id):
        """ Get a client from its ID. 
        Returns client object, or False if no client
        """
        mcli = MClient.query.get(client_id)
        if mcli is None:
            return False

        cli = Client(mcli.client_name)
        cli.ID = mcli.id
        cli._mcli = mcli
        return cli

    @staticmethod
    def getClientFromName(cliname, match=False):
        """ Gets a client list that have the name equals 'client_name'
        If match=False, any client that have aby part of name matching 'client_name' will be returned.
        If match=True, only the exact matches will be returned """

        if match == True:
            mclis = MClient.query.filter_by(client_name=cliname)
        else:
            mclis = MClient.query.filter(or_(MClient.client_name.startswith(cliname),MClient.client_name.endswith(cliname)))

        if mclis is None:
            return False

        clis = []
        
        for mcli in mclis:
            cli = Client(mcli.client_name)
            cli.ID = mcli.id
            cli._mcli = mcli
            clis.append(cli)

        return clis
    
            

    
