'''
Created on Dec 4, 2012

@author: kpaskov
'''
from model_old_schema.model import get_first, get
import datetime
import string

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def get_feature_by_name(name, session=None):
    """
    Get a feature by its name.
    """  
    
    from model_old_schema.feature import Feature

    def f(session):
        
        feature = get_first(Feature, session, name=name.upper())
        if feature is not None and not feature.type=='chromosome':
            return feature
        
        feature = get_first(Feature, session, gene_name=name.upper())
        if feature is not None:
            return feature
        
        feature = session.query(Feature).filter(Feature.alias_names.contains(name.upper())).first()
        if feature is not None:
            return feature  
        
        return None                              
    
    return f if session is None else f(session)
    
def get_reftemps(session=None):
    
    from model_old_schema.reference import RefTemp

    def f(session):
        return get(RefTemp, session)
    
    return f if session is None else f(session)

def validate_genes(gene_names, session=None):
    """
    Convert a list of gene_names to a mapping between those gene_names and features.
    """            
    
    from model_old_schema.feature import Feature

    def f(session):
        if gene_names is not None and len(gene_names) > 0:
            upper_gene_names = [x.upper() for x in gene_names]
            fs = set(session.query(Feature).filter(Feature.name.in_(upper_gene_names)).all())
            fs.update(session.query(Feature).filter(Feature.gene_name.in_(upper_gene_names)).all())
                
            name_to_feature = {}
            for f in fs:
                name_to_feature[f.name] = f
                name_to_feature[f.gene_name] = f
                
            extraneous_names = name_to_feature.keys()
            for name in upper_gene_names:
                if name.upper() in extraneous_names:
                    extraneous_names.remove(name.upper())
                    
            for name in extraneous_names:
                del name_to_feature[name]
                 
            return name_to_feature
        else:
            return {}
        
    return f if session is None else f(session)

def find_genes_in_abstract(pubmed_id, session=None):
    """
    Convert a list of gene_names to a mapping between those gene_names and features.
    """            
    
    from model_old_schema.reference import RefTemp

    def f(session):
        word_to_feature = {}
        features = []
        
        r = get_first(RefTemp, pubmed_id=pubmed_id, session=session)
        a = str(r.abstract).lower().translate(string.maketrans("",""), string.punctuation)
        words = a.split()
        
        for word in words:
            if not word in word_to_feature and not is_number(word):
                f = get_feature_by_name(word, session)
                word_to_feature[word] = f
                if f is not None and not f.type == 'chromosome':
                    features.append(f)
        return features
        
    return f if session is None else f(session)

class HistoryEntry():
    def __init__(self, date):
        self.date = date
        self.ref_count = 0
        self.refbad_count = 0
        
    def inc_ref_count(self):
        self.ref_count = self.ref_count + 1
    
    def inc_refbad_count(self):
        self.refbad_count = self.refbad_count + 1
    

def get_recent_history(session=None):
    """
    Get a user's recent history.
    """       
    from model_old_schema.reference import Reference, RefBad

    def f(session):
        min_date = datetime.date.today() - datetime.timedelta(days=10)
        refs = session.query(Reference).filter_by(created_by = session.user).filter(Reference.date_created >= min_date)
        refbads = session.query(RefBad).filter_by(created_by = session.user).filter(Reference.date_created >= min_date)
        
        history = {}
        today = datetime.date.today()
        for i in range(10):
            new_date = today - datetime.timedelta(days=i)
            history[new_date] = HistoryEntry(new_date)
        
        for ref in refs:
            if ref.date_created in history:
                history[ref.date_created].inc_ref_count()
                
        for refbad in refbads:
            if refbad.date_created in history:
                history[refbad.date_created].inc_refbad_count()
                
        return history
        
    return f if session is None else f(session)