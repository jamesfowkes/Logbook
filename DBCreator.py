import logging
import sys

from DBError import DBError

## Table Definitions

gliders = [
    ['ID', '%s INTEGER PRIMARY KEY'],
    ['Trigraph', '%s TEXT'],
    ['Comp_No', '%s TEXT'],
    ['Reg', '%s TEXT'],
    ['Type', '%s INTEGER'],
    ['Notes', '%s TEXT'],
    ## Define key constraints
    ['Type', 'FOREIGN KEY(%s) REFERENCES glidertypes(id)'],
    ]

manufacturers = [
    ['Name', '%s TEXT PRIMARY KEY']
    ]
    
glidertypes = [
    ['id', '%s INTEGER PRIMARY KEY'],
    ['Manufacturer', '%s TEXT'],
    ['Name', '%s TEXT'],
    ## Define key constraints
    ['Manufacturer', 'FOREIGN KEY(%s) REFERENCES manufacturers(Name)'],
    ]
    
locations = [
    ['Name', '%s TEXT PRIMARY KEY'],
    ['Lat', '%s TEXT'],
    ['Long', '%s TEXT']
    ]

flights = [
    ['number', '%s INTEGER'],
    ['datetime', '%s INTEGER'],
    ['GliderID', '%s INTEGER'],
    ['Location', '%s TEXT'],
    ['Capacity', '%s TEXT'],
    ['Duration', '%s INTEGER'],
    ['Launch', '%s TEXT'],
    ['Km_flown', '%s TEXT'],
    ['Notes', '%s TEXT'],
    ## Define key constraints
    ['number, datetime', 'PRIMARY KEY(%s)'],
    ['GliderID', 'FOREIGN KEY(%s) REFERENCES gliders(ID)'],
    ['Location', 'FOREIGN KEY(%s) REFERENCES locations(Name)'],
    ]

## Database tables in order of dependency

tables = {
    'manufacturers': manufacturers,
    'glidertypes': glidertypes,
    'gliders': gliders,
    'locations': locations,
    'flights': flights,
    }

sql = {
    "getTables":                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name",
    "createTable":                  "CREATE TABLE IF NOT EXISTS %s (%s)",
    "createDefaultLocations":       "INSERT INTO locations (Name, Lat, Long) VALUES (%s)",
    "createDefaultGliders":         "INSERT INTO gliders (Trigraph, Comp_No, Reg, Type, Notes) VALUES (%s)",
    "createDefaultGliderTypes":     "INSERT INTO glidertypes (id, Manufacturer, Name) VALUES (%s)",
    "createDefaultManufacturers":   "INSERT INTO manufacturers (Name) VALUES ('%s')"
    }

locations = ["'Cranwell', '53.0419' , '-0.493333'", "'Portmoak', '56.189038' , '-3.321831'"]

types = [
    "0, 'Schleicher', 'K13'",
    "1, 'Grob', 'Acro'", 
    "2, 'Grob', 'Astir CS'",
    "3, 'Schleicher', 'K18'",
    "4, 'Schleicher', 'K21'",
    "5, 'Slingsby', 'Skylark'",
    "6, 'Grob', 'Astir CS77'"]
    
gliders = [
    "'HPE', '', '', 0, ''",
    "'JPY', 'R59', 'G-CJPY', 0, ''",
    "'JRW', 'NU2', 'G_NUGC', 1, ''",
    "'KBD', 'NU', '', 2, ''",
    "'FTR', 'NU', 'G-CFTR', 6, ''",
    "'JLR', 'R57', 'G-CJLR', 2, ''",
    "'KMW', 'R18', 'G-CKMW', 4, ''",
    "'JPZ', 'R56', 'G-CJPZ', 3, ''",
    "'CCS', '', '', 5, ''"]
    
manufs = ['Schleicher', 'Grob', 'Slingsby', 'Schempp-Hirth']

class DBCreator:                                       
                                                      
    def __init__(self, db):
        if db is None:
            raise DBError("DBCreator.__init__", "No database object provided")

        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        
    def createMissingTables(self):
        
        """Create the database tables"""
        self.__createMissingTables__()
    
        if len(self.errors) > 0:
            raise DBError("createMissingTables", "Error(s) occured while creating tables")
    
    def populateDefaults(self):
        
        """Populate the tables with default data """
        self.__populateDefaults__()
    
        if len(self.errors) > 0:
            raise DBError("populateDefaults", "Error(s) occured while populating tables")
    
    
    def scanForErrors(self):
    
        self.errors = []
    
        """Scans database tables for missing columns"""
        for name, tabledef in tables.items():
            dbColumns = self.__getColumnsFromDb__(name)
            
            for column, type in tabledef:
                if column not in dbColumns:
                    self.errors.append("Column '%s' not in table '%s'" % (column, name))
        
        return (len(self.errors) > 0)
     
    def __populateDefaults__(self):
    
        self.errors = []
        
        try:
            if self.__tableIsEmpty__("manufacturers"):
                for manuf in manufs:
                    self.db.execute(sql['createDefaultManufacturers'] % manuf)
            if self.__tableIsEmpty__("glidertypes"):
                for type in types:
                    self.db.execute(sql['createDefaultGliderTypes'] % type)                
            if self.__tableIsEmpty__("locations"):
                for location in locations:
                    self.db.execute(sql['createDefaultLocations'] % location)
            if self.__tableIsEmpty__("gliders"):
                for glider in gliders:
                    self.db.execute(sql['createDefaultGliders'] % glider)
            
        except Exception as e:
            self.errors.append(str(e))

    def __createMissingTables__(self):
        """Create any missing tables"""

        self.errors = []
        
        for name, tabledef in tables.items():
            columndefs = self.__getColumnDefString__(tabledef)
            try:
                _sql = sql['createTable'] % (name, columndefs)
                self.logger.info("Creating table %s..." % name)
                self.logger.info("SQL: '%s'" % _sql)
                self.db.execute(_sql)
            except Exception as e:
                self.errors.append(str(e))
        
    def __getTablesFromDb__(self):
        """Pulls list of tables from the database"""
        
        self.errors = []
        
        try:
            self.db.execute(sql['getTables'])
            return [tabledef[0] for tabledef in self.db.fetchall()]
        except:
            return[]
        
    
    def __getColumnsFromDb__(self, table):
        """Pulls list of columns from a database table"""
        
        try:
            self.db.execute("PRAGMA table_info(%s)" % table)
            return [columndef[1] for columndef in self.db.fetchall()]
        except:
            return []
    
    def __createColumnDef__(self, columndef):
        """Creates SQL compliant column definition 
        from single local column definition"""
        try:
            sqlcolumndef = columndef[1] % columndef[0]
        except:
            print columndef
            
        return sqlcolumndef
        
    def __getColumnDefString__(self, tabledef):
        """Creates SQL compliant column definition
        for entire table from descriptions at head of file"""
        
        columndefs = ", ".join( [self.__createColumnDef__(column) for column in tabledef] )
        return columndefs
   
    def __tableIsEmpty__(self, table):
        _sql = "SELECT COUNT(*) AS row_count FROM %s" % table
        result = self.db.execute(_sql).fetchone()
        return result['row_count'] == 0
        
def main(argv = None):
    """Standalone run for GLOG_DB_Create"""

if __name__ == "__main__":
    main()