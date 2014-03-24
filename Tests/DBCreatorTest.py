import unittest
import sqlsoup

from Logbook import DBCreator
from Logbook import DBError
from TestConstants import TEST_CONSTANTS

class DBCreatorTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def testCreateWithNoDBRaisesError(self):
        db = None

        with self.assertRaises(DBError.DBError) as context:
            DBCreator.DBCreator(None)
            
    def testCreateWithValidSucceeds(self):
        db = sqlsoup.SQLSoup("sqlite:///%s" % TEST_CONSTANTS['DatabasePath'])

        DBCreator.DBCreator(db)
            
if __name__ == '__main__':
    unittest.main()
