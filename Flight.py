from sqlalchemy import asc, desc
from datetime import datetime, date

from DBRecord import DBRecord

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
        
class Flight(DBRecord):
        
    def __init__(self, db, table, datetime, gliderID, location_name, capacity, duration, launch, km_flown, notes):
        self.db = db
        data_dict = {
            'number':0,
            'datetime':datetime,
            'GliderID':gliderID,
            'Location':location_name,
            'Capacity':capacity,
            'Duration':duration,
            'Launch':launch,
            'Km_flown':km_flown,
            'Notes':notes}
            
        DBRecord.__init__(self, table, data_dict)

    def Create(self):
        self.Set('number', self.__getNextFlightNumber())
        DBRecord.Create(self, self.db)
        
    def __getNextFlightNumber(self):
        try:
            datetime = self.Get('datetime')
            qry = self.db.flights.filter(self.db.flights.datetime == datetime.isoformat(" "))
            qry = qry.order_by(desc(self.db.flights.number)).first()
            return qry.number + 1
        except AttributeError:
            return 0
            