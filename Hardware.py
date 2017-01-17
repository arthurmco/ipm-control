""" Returns hardware information """

from Cliente import Client

class Hardware(object):
    def __init__(self, client, hw_name, hw_desc):
        self.ID = False
        self.client = client
        self.name = hw_name
        self.desc = hw_desc

    def addIntoDatabase(self):
        """ Adds into database. Returns hardware ID """
        pass

    def removeFromDatabase(self):
        """ Removes from database. Sets ID to False """
        pass

    @staticmethod
    def getHardwareByID(hw_id):
        """ Returns hardware by its ID, or False if no hardware """
        pass

    @staticmethod
    def getHardwaresByName(hw_name, match=False):
        """ Returns hardware by name.
        If match=False, then it will return every hardware that has 'hw_name' into name
        If match=True, only exact matches will be returned """
        pass

    @staticmethod
    def getHardwaresByClient(client):
        """ Get hardware that belong to client 'client' """
        pass
