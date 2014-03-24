import os
import sqlsoup

from DBCreator import DBCreator
from DBError import DBError
        
class DBAccess:
    """Database description and access layer"""

    def __init__(self, path):
        self.dbpath = path
        self.__tryConnection__()
        
        if self.getConnectionState():
            self._dbCreator = DBCreator(self.db)
    
    def commit(self):
        self.db.commit()
        
    def scanForErrors(self):
        self._dbCreator.scanForErrors()
        
    def getConnectionState(self):
        return self.db is not None
        
    def getDatabasePath(self):
        return self.dbpath
    
    def createMissingTables(self):
        try:
            self._dbCreator.createMissingTables()
        except DBError:
            print self._dbCreator.errors
    
    def populateDefaults(self):
        try:
            self._dbCreator.populateDefaults()
        except:
            print self._dbCreator.errors
    
    def __tryConnection__(self):

        if not os.path.isfile(self.dbpath):
            raise DBError("__tryConnection__", "%s was not found" % self.dbpath)

        try:
            self.db = sqlsoup.SQLSoup("sqlite:///%s" % self.dbpath)
        except:
            self.db = None
            raise DBError("__tryConnection__", "Could not connect to %s" % self.dbpath)
        
def main(argv = None):
    pass

if __name__ == "__main__":
    main()