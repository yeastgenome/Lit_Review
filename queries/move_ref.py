'''
Created on Dec 4, 2012

@author: kpaskov
'''
from modelOldSchema.model import get_first

def move_reftemp_to_refbad(pubmed_id):
    """"
    Remove reference from the RefTemp table and add it to the RefBad table.
    """ 
    
    from modelOldSchema.reference import RefTemp, RefBad

    def x(session):        
        reftemp = get_first(session, RefTemp, pubmed_id=pubmed_id)
        refbad = RefBad(pubmed_id)
        
        session.add(refbad)
        session.delete(reftemp)
        session.commit()
        return True
    return x
            
def move_refbad_to_reftemp(pubmed_id):
    """"
    Remove reference from the RefBad table and add it to the RefTemp table.
    """     
    
    from modelOldSchema.reference import RefTemp, RefBad
    
    def x(session):       
        refbad = get_first(session, RefBad, pubmed_id=pubmed_id)
        reftemp = RefTemp(pubmed_id, None)
            
        session.add(reftemp)
        session.delete(refbad)
        session.commit()
        return True
    return x
            
def move_reftemp_to_ref(pubmed_id):
    """
    Remove reference from the RefTemp table, create a full Reference, and add it to the Reference table.
    """
    
    from modelOldSchema.reference import RefTemp, Reference

    def x(session):
        reftemp = get_first(session, RefTemp, pubmed_id=pubmed_id)
        ref = Reference(pubmed_id, session)
            
        session.add(ref)
        session.delete(reftemp)
        session.commit()
        return True
    return x
            
def move_ref_to_reftemp(pubmed_id):
    """
    Remove reference from the Reference table and add it to the RefTemp table.
    """
    
    from modelOldSchema.reference import RefTemp, Reference

    def x(session):        
        ref = get_first(session, Reference, pubmed_id=pubmed_id)
        reftemp = RefTemp(pubmed_id, None)
            
        session.add(reftemp)
        session.delete(ref)
        session.commit()
        return True
    return x
