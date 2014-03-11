import os
import sqlsoup

from DBCreator import DBCreator
from DBError import DBError
        
class DBAccess:
    """Database description and access layer for GLOG"""

    def __init__(self, path):
        self.dbpath = path
        self._lastError_ = ''
        self.__tryConnection__()
        
        if self.getConnectionState():
            self._dbCreator = DBCreator(self.db)

    def scanForErrors(self):
        self._dbCreator.scanForErrors()
        
    def getConnectionState(self):
        return self.db is not None
        
    def getDatabasePath(self):
        return self.dbpath
    
    def getLastError(self):
        return self._lastError_

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

    """ CREATE Operations """
    
    def CreateGliderType(self, manufacturer, name):
        
        result = True
        
        try:
            self.db.glidertypes.insert(
                Manufacturer = manufacturer,
                Name = name)
                
            self.db.commit()
            
        except:
            result = False
            
        return result
        
    def CreateManufacturer(self, name):
        
        result = True
        
        try:
            self.db.manufacturers.insert(
                Name = name)
                
            self.db.commit()
            
        except:
            result = False
            
        return result
        
    def CreateLocation(self, name, lat, long):
        
        result = True
        
        try:
            self.db.locations.insert(
                Name = name,
                Lat = lat,
                Long = long)
                
            self.db.commit()
            
        except:
            result = False
            
        return result
        
    
    def __tryConnection__(self):
        try:
            self.db = sqlsoup.SQLSoup("sqlite:///%s" % self.dbpath)
        except:
            self._lastError_ = "Could not connect to %s" % self.dbpath
            self.db = None
        
def main(argv = None):
    """Standalone test for GLOG_DB_Access"""
    test = DBAccess("testlog.db")

if __name__ == "__main__":
    main()