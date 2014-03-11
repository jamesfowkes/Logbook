from random import randint

class Location:

    
    @staticmethod
    def getRandomLocation(db):
        results = db.execute("SELECT Name FROM locations").fetchall()
        maxID = len(results) - 1
               
        return str( results[randint(0, maxID)]['Name'] )
        
    @classmethod
    def findByName(cls, db, name):
        location = db.locations.filter(db.locations.Name.like("%s%%" % name)).one()
        return cls(location.Name, location.Lat, location.Long)
        
    def __init__(self, name, lat, long):
        self.name = name
        self.lat = lat
        self.long = long
     
    def Create(self, db):
        
        result = True
        self.db = db.db
        try:
            self.db.locations.insert(
                Name = self.name,
                Lat = self.lat,
                Long = self.long)
                
            self.db.commit()
            
        except:
            raise
            #result = False
            
        return result
    
    def Delete(self):
    
        result = True
        
        try:
            location = self.db.locations.filter_by(Name=self.name).one()
            self.db.delete( location )
            self.db.commit()
            
        except:
            result = False
            
        return result
        
    def Update(self):
    
        result = True
        
        try:
            location = self.db.locations.filter_by(Name=self.name).one()
            location.Name = self.name
            location.Lat = self.lat
            location.Long = self.long

            self.db.commit()
            
        except:
            result = False
            
        return result
