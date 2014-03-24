import re
import datetime

import random
from random import randint
from DateUtils import DateUtils

from Flight import Flight
from Glider import Glider, GliderSearch
from Location import Location

class ShorthandParseException(Exception):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
    
    def __str__(self):
        return self.msg + " (" + self.expr + ")"

class ShorthandParser():

    def __init__(self, shorthand, db):
        self.shorthand = shorthand
        self.db = db
    
    @staticmethod
    def generateRandomEntry(db):
        shorthand = "A"
    
        randomDate = DateUtils.randomDate(datetime.date(2013, 6, 1), datetime.date.today())
        shorthand += "D" + randomDate.strftime("%d%m%y")
        shorthand += "G" + Glider.getRandomTrigraphOrCompNo(db)
        shorthand += "L" + Location.getRandomLocation(db)[:3]
        nFlights = randint(1,4);
        shorthand += "N" + str(nFlights)
        shorthand += "P" + str(randint(1,2))
        shorthand += "T"
        for i in range(nFlights):
            shorthand += "%02d" % randint(3, 20)
        
        shorthand += random.choice("WA")
        
        shorthand = shorthand.upper()
        
        shorthand += "NRandom Notes " if random.choice([True, False]) else ""
        
        return shorthand
        
    def getFlights(self):
        
        print self.shorthand
        """Create a flight object from a shorthand command"""
        regexp = """
            A
            (D[0-9]{6})?
            (G[A-Z0-9]{2,3})
            (L[A-Z]{3})
            (N[0-9]{1,2})
            (P1|P2)
            T([0-9]*)
            (W|A)?
            (N.*)?
            """
            
        regexp = ''.join(regexp.split())
        try:
            matches = re.match(regexp, self.shorthand).groups()	
        except AttributeError:
            raise ShorthandParseException(self.shorthand, "Failed to parse shorthand")
            
        expectedMatches = [
            "Date",
            "Identifier",
            "Location",
            "Number Of Flights",
            "Capacity",
            "Times",
            "Launch Type",
            "Notes"
        ]

        successfulParseCount = 0
        for idx, expectedMatch in enumerate(expectedMatches):
            if matches[idx] is not None:
                match = matches[idx][1:]
                if expectedMatch == "Identifier":
                    gliders = GliderSearch.find(self.db, GliderSearch.TRIGRAPH, match)
                    if len(gliders) == 0:
                        gliders = GliderSearch.find(self.db, GliderSearch.COMPNO, match)
                        if len(gliders) == 0:
                            raise ShorthandParseException(matches[idx], "Could not parse this %s" % expectedMatch )
                    
                    gliderID = random.choice(gliders).Get('ID')
                        
                elif expectedMatch == "Date":
                    try:
                        flightDate = datetime.datetime.strptime(match, "%d%m%y")
                    except:
                        raise ShorthandParseException(matches[idx], "Could not parse this %s" % expectedMatch )
                               
                elif expectedMatch == "Location":
                    location_name = Location.findByName(self.db, match).Get('name')
                    if location_name is None:
                        raise ShorthandParseException(matches[idx], "Could not parse this %s" % expectedMatch)
                        
                elif expectedMatch == "Number Of Flights":
                    try:
                        number_of_flights = int(match)
                    except:
                        raise ShorthandParseException(matches[idx], "Could not parse this %s" % expectedMatch)
                        
                elif expectedMatch == "Capacity":
                    capacity = "P" + match
                    
                elif expectedMatch == "Times":
                    times = self.__parseQuickEntryTimes(matches[idx])
                    if times is None:
                        raise ShorthandParseException(matches[idx], "Could not parse this as %s" % expectedMatch)
                        
                elif expectedMatch == "Launch Type":
                    launchtype = match
                elif expectedMatch == "Notes":
                    notes = match
        
            else:
                ## Date, launch type and notes are not required
                if expectedMatch == "Launch Type":
                    launchtype = "W" # Default to winch type
                elif expectedMatch == "Notes":
                    notes = ""
                elif expectedMatch == "Date":
                    flightDate = date.today()
                else:
                    raise ShorthandParseException(self.shorthand, "Expected entry %s was not found" % expectedMatch)

        if len(times) != number_of_flights:
            raise ShorthandParseException(self.shorthand, "Number of flights (%d) and provided times (%d) do not match." % (number_of_flights, len(times)))
        
        flights = [Flight(self.db, self.db.flights, flightDate, gliderID, location_name, capacity, t, launchtype, 0, notes) for t in times]
        
        return flights
    
    @staticmethod
    def __parseQuickEntryTimes(times):
        """ Parses a numeric string in the form "99999999..." where each 99
        represents a flight time in minutes """
        
        try:
            # Split and convert to integers
            integerTimes = [int(times[i:i+2]) for i in range(0, len(times), 2)]
        except ValueError:
            raise

        return integerTimes