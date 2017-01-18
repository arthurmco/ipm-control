""" Returns hardware information """

from Cliente import Client
from models.Models import db, MHardware

class Hardware(object):
    def __init__(self, client, hw_name, hw_desc):
        self.ID = False
        self.client = client
        self.name = hw_name
        self.desc = hw_desc
        self._mcli = None

    def addIntoDatabase(self):
        """ Adds into database. Returns hardware ID """
        self._mcli = MHardware(self.client.ID, self.name, self.desc)
        db.session.add(self._mcli)
        db.session.commit()
        self.ID = self._mcli.id
        return self.ID

    def updateIntoDatabase(self):
        if self._mcli is None:
            return self.addIntoDatabase()

        self._mcli.client_id = self.client.ID
        self._mcli.hw_name = self.hw_name
        self._mcli.hw_desc = self.hw_desc
        db.session.add(self._mcli)
        db.session.commit()
    
    def removeFromDatabase(self):
        """ Removes from database. Sets ID to False """
        db.session.delete(self._mcli)
        db.session.commit()
        self.ID = False

    @staticmethod
    def getHardwareByID(hw_id):
        """ Returns hardware by its ID, or False if no hardware """
        mcli = MHardware.query.get(hw_id)
        if mcli is None:
            return False

        hw = Hardware(Client.getClientFromID(mcli.client_id),
                      mcli.hw_name, mcli.hw_desc)
        hw.ID = mcli.ID
        hw._mcli = mcli
        return hw

    @staticmethod
    def getHardwaresByName(hw_name, match=False):
        """ Returns hardware by name.
        If match=False, then it will return every hardware that has 'hw_name' into name
        If match=True, only exact matches will be returned """
         if match == True:
            mclis = MHardware.query.filter_by(hw_name=hw_name)
        else:
            mclis = MHardware.query.filter(or_(MHardware.hw_name.startswith(hw_name),MHardware.hw_name.endswith(hw_name)))

        if mclis is None:
            return False

        clis = []
        
        for mcli in mclis:
            hw = Hardware(Client.getClientFromID(mcli.client_id),
                          mcli.hw_name, mcli.hw_desc)
            hw.ID = mcli.ID
            hw._mcli = mcli
            clis.append(hw)

        return clis

    @staticmethod
    def getHardwaresByClient(client):
        """ Get hardware that belong to client 'client' """
        mclis = MHardware.query.filter_by(client_id=client.ID)
        
        if mclis is None:
            return False

        clis = []
        
        for mcli in mclis:
            hw = Hardware(Client.getClientFromID(mcli.client_id),
                          mcli.hw_name, mcli.hw_desc)
            hw.ID = mcli.ID
            hw._mcli = mcli
            clis.append(hw)

        return clis

