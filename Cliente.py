""" Dados sobre clientes e hardwares """

class Client(object):
    """ Define um cliente """
    def __init__(self, name):
        self.ID = False
        self.name = name

    def addIntoDatabase(self):
        """ Adds into database. Returns client ID """
        pass

    def removeFromDatabase(self):
        """ Removes from database. Sets ID to False """
        pass

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
        pass

    @staticmethod
    def getClientFromName(client_name, match=False):
        """ Gets a client list that have the name equals 'client_name'
        If match=False, any client that have aby part of name matching 'client_name' will be returned.
        If match=True, only the exact matches will be returned """
        pass

    
