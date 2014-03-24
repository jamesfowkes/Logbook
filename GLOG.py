from Flight import Flight
from ShorthandParser import ShorthandParser, ShorthandParseException
from DBAccess import DBAccess
from DBError import DBError

import sys
    
ADD_FLIGHT = 'A'

__constants__ = {
    'DatabasePath' : 'logbook.db'
}

class ConsoleHandler:

    def __init__(self, db):

        self.db = db
        self.exit = False
        
    def run(self):

        while (self.exit == False):
            cmd = raw_input('Next command:')
            
            if (cmd.startswith(ADD_FLIGHT)):
                self.addFlightFromInput(cmd)
            elif (cmd.upper() == "TEST") or (cmd.upper() == "T"):
                cmd = ShorthandParser.generateRandomEntry(self.db.db)
                self.addFlightFromInput(cmd)
            elif (cmd == "exit"):
                self.exit = True
    
    def addFlightFromInput(self, cmd):
        try:
            newFlights = ShorthandParser(cmd, self.db.db).getFlights()
            for f in newFlights:
                f.Create()
                
        except ShorthandParseException as e:
            print "Error parsing shorthand: %s" % e
    
def VerifyDatabase(db):
    if db.scanForErrors():
        print("Database errors found:")
        for error in db.errors:
            print error
        sys.exit(0)

def GetDatabase():
    """Attempts to get handle for database"""

    try:
        db = DBAccess(__constants__['DatabasePath'])
    except DBError as e:
        print e.msg
        for error in db.errors:
            print error + "\n"
        sys.exit(0)
    
    return db
    
def main(argv = None):

    try:
        db = GetDatabase()
        db.createMissingTables()
        db.populateDefaults()
        
        VerifyDatabase(db)
        
        if (argv is None):
            ## Console application
            argv = sys.argv
            ConsoleHandler(db).run()
        else:
            CommandHandler(db).run()
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        sys.exit(0)
        
if __name__ == "__main__":
    main()