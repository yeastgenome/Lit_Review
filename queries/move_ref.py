'''
Created on Dec 4, 2012

@author: kpaskov
'''
from modelOldSchema.model import get_first

def move_reftemp_to_refbad(pubmed_id, session=None):
    """"
    Remove reference from the RefTemp table and add it to the RefBad table.
    """ 
    
    from modelOldSchema.reference import RefTemp, RefBad

    def f(session):        
        reftemp = get_first(RefTemp, session, pubmed_id=pubmed_id)
        refbad = RefBad.as_unique(session, pubmed_id=pubmed_id)
        
        session.add(refbad)
        session.delete(reftemp)
        return True
    
    return f if session is None else f(session)

            
def move_refbad_to_reftemp(pubmed_id, session=None):
    """"
    Remove reference from the RefBad table and add it to the RefTemp table.
    """     
    
    from modelOldSchema.reference import RefTemp, RefBad
    
    def f(session):       
        refbad = get_first(RefBad, session, pubmed_id=pubmed_id)
        reftemp = RefTemp.as_unique(session, pubmed_id = pubmed_id)
            
        session.add(reftemp)
        session.delete(refbad)
        return True
    
    return f if session is None else f(session)
            
def move_reftemp_to_ref(pubmed_id, session=None):
    """
    Remove reference from the RefTemp table, create a full Reference, and add it to the Reference table.
    """
    
    from modelOldSchema.reference import RefTemp, Reference

    def f(session):
        reftemp = get_first(RefTemp, session, pubmed_id=pubmed_id)
        ref = Reference.as_unique(session, pubmed_id=pubmed_id)
            
        session.add(ref)
        session.delete(reftemp)
        return True
  
    return f if session is None else f(session)
            
def move_ref_to_reftemp(pubmed_id, session=None):
    """
    Remove reference from the Reference table and add it to the RefTemp table.
    """
    
    from modelOldSchema.reference import RefTemp, Reference

    def f(session):        
        ref = get_first(Reference, session, pubmed_id=pubmed_id)
        reftemp = RefTemp.as_unique(session, pubmed_id=pubmed_id)
            
        session.add(reftemp)
        session.delete(ref)
        return True
    
    return f if session is None else f(session)

class MoveRefException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)