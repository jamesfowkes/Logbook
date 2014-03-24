import unittest

from Logbook import DBAccess
from Logbook import DBError
from LogbookTestConstants import TEST_CONSTANTS

class DBAccessTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def testAccessWithInvalidPathRaisesError(self):
    
        access = None
        with self.assertRaises(DBError.DBError) as context:
            access = DBAccess.DBAccess(TEST_CONSTANTS['InvalidPath'])
        
        self.assertTrue(access == None)
        
    def testAccessWithValidPathSucceeds(self):
        access = DBAccess.DBAccess(TEST_CONSTANTS['DatabasePath'])

        self.assertTrue(access.getConnectionState())
        
if __name__ == '__main__':
    unittest.main()
