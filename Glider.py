import random
from random import randint
        
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
        
        gliders = [Glider(r.ID, r.Trigraph, r.Comp_No, r.Reg, r.Type, r.Notes) for r in results]
        return gliders
        
class Glider:

    @staticmethod
    def getRandomTrigraphOrCompNo(db):
        results = db.execute("SELECT Trigraph, Comp_No FROM gliders").fetchall()
        maxID = len(results) - 1
        
        (trigraph, comp_no) = (results[randint(0, maxID)]['Trigraph'], results[randint(0, maxID)]['Comp_No'])
        
        if len(comp_no) > 0:
            return random.choice((trigraph, comp_no))
        else:
            return trigraph
    
    def __init__(self, id, trigraph, comp_no, reg, type, notes):
        self.ID = id
        self.trigraph = trigraph
        self.comp_no = comp_no
        self.reg = reg
        self.type = type
        self.notes = notes
        
    def Create(self, db):
        
        result = True
        self.db = db.db
        try:
            self.db.gliders.insert(
                Trigraph = self.trigraph,
                Comp_No = self.comp_no,
                Reg = self.reg,
                Type = self.type,
                Notes = self.notes)
                
            self.db.commit()
            
        except:
            raise
            #result = False
            
        return result
    
    def Delete(self):
    
        result = True
        
        try:
            glider = self.db.gliders.filter_by(Trigraph=self.trigraph).one()
            self.db.delete( flight )
            self.db.commit()
            
        except:
            result = False
            
        return result
        
    def Update(self):
    
        result = True
        
        try:
            glider = self.db.gliders.filter_by(Trigraph=self.trigraph).one()
            glider.Comp_No = self.comp_no,
            glider.Reg = self.reg,
            glider.Type = self.type,
            glider.Notes = self.notes

            self.db.commit()
            
        except:
            result = False
            
        return result
