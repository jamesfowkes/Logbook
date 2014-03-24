import random
from random import randint

from DBRecord import DBRecord

class GliderSearch:
    TRIGRAPH = 1
    COMPNO = 2

    class SearchError(Exception):
        def __init__(self, expr, msg):
            self.expr = expr
            self.msg = msg
    
    @staticmethod
    def find(db, findBy, criteria):
        try:
            if (findBy == GliderSearch.TRIGRAPH):
                results = db.gliders.filter_by(Trigraph=criteria)
            elif (findBy == GliderSearch.COMPNO):
                results = db.gliders.filter_by(Comp_No=criteria)
            else:
                raise GliderSearch.SearchError("SearchError", "Unknown find criteria type")
        except:
            raise
        
        gliders = [Glider(db.gliders, r.ID, r.Trigraph, r.Comp_No, r.Reg, r.Type, r.Notes) for r in results]
        return gliders
        
class Glider(DBRecord):

    @staticmethod
    def getRandomTrigraphOrCompNo(db):
        results = db.execute("SELECT Trigraph, Comp_No FROM gliders").fetchall()
        maxID = len(results) - 1
        
        (trigraph, comp_no) = (results[randint(0, maxID)]['Trigraph'], results[randint(0, maxID)]['Comp_No'])
        
        if len(comp_no) > 0:
            return random.choice((trigraph, comp_no))
        else:
            return trigraph
    
    def __init__(self, table, id, trigraph, comp_no, reg, type, notes):
        
        data_dict = {
            'ID':id,
            'trigraph':trigraph,
            'comp_no':comp_no,
            'reg':reg,
            'type':type,
            'notes':notes}
            
        DBRecord.__init__(self, table, data_dict)

