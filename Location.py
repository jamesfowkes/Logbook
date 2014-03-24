from random import randint

from DBRecord import DBRecord

class Location(DBRecord):

    
    @staticmethod
    def getRandomLocation(db):
        results = db.execute("SELECT Name FROM locations").fetchall()
        maxID = len(results) - 1
               
        return str( results[randint(0, maxID)]['Name'] )
        
    @classmethod
    def findByName(cls, db, name):
        location = db.locations.filter(db.locations.Name.like("%s%%" % name)).one()
        return cls(db.locations, location.Name, location.Lat, location.Long)
        
    def __init__(self, table, name, lat, long):
    
        data_dict = {
            'name':name,
            'lat':lat,
            'long':long}
            
        DBRecord.__init__(self, table, data_dict)
