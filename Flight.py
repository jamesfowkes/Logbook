from sqlalchemy import asc, desc
from datetime import datetime, date

class FlightSearch:

    #Search fields
    DATERANGE = 0
    TRIGRAPH = 1
    LOCATION = 2
    CAPACITY = 3
    DURATIONRANGE = 4
    LAUNCH = 5
    NOTES = 6
    
    def __init__(self, field, data):
        pass
        
class Flight:
        
    def __init__(self, datetime, gliderID, location_name, capacity, duration, launch, km_flown, notes):
        self.datetime = datetime
        self.gliderID = gliderID
        self.location_name = location_name
        self.capacity = capacity
        self.duration = duration
        self.launch = launch
        self.km_flown = km_flown
        self.notes = notes
  
    def Create(self, db):
        
        result = True
        self.db = db.db
        try:
            self.number = self.__getNextFlightNumber()
            self.db.flights.insert(
                number = self.number,
                datetime = self.datetime,
                GliderID = self.gliderID,
                Location = self.location_name,
                Capacity = self.capacity,
                Duration = self.duration,
                Launch = self.launch,
                Km_flown = self.km_flown,
                Notes = self.notes)
                
            self.db.commit()
            
        except:
            raise
            
        return result
    
    def Delete(self):
    
        result = True
        
        try:
            flight = self.db.flights.filter_by(number=self.number, datetime=self.datetime).one()
            self.db.delete( flight )
            self.db.commit()
            
        except:
            result = False
            
        return result
        
    def Update(self):
    
        result = True
        
        try:
            flight = self.db.flights.filter_by(number=self.number, datetime=self.datetime).one()
            flight.number = self.number
            flight.datetime = self.datetime
            flight.GliderID = self.gliderID
            flight.Location = self.location_name
            flight.Capacity = self.capacity
            flight.Duration = self.duration
            flight.Launch = self.launch
            flight.Km_flown = self.km_flown
            flight.Notes = self.notes
            self.db.commit()
            
        except:
            result = False
            
        return result
        
    def __getNextFlightNumber(self):
        try:
            qry = self.db.flights.filter(self.db.flights.datetime == self.datetime.isoformat(" "))
            qry = qry.order_by(desc(self.db.flights.number)).first()
            return qry.number + 1
        except AttributeError:
            return 0
            