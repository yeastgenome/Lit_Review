'''
Created on Dec 4, 2012

@author: kpaskov
'''
from modelOldSchema.model import get_first, get

def get_feature_by_name(name):
    """
    Get a feature by its name.
    """
    
    from modelOldSchema.feature import Feature

    def x(session):
        f = get_first(session, Feature, name=name.upper())
        if f:
            return f
        else:
            return get_first(session, Feature, gene_name=name.upper())
    return x
    
def get_reftemps():
    
    from modelOldSchema.reference import RefTemp

    def x(session):
        return get(session, RefTemp)
    return x

def validate_genes(gene_names):
    """
    Convert a list of gene_names to a mapping between those gene_names and features.
    """            
    
    from modelOldSchema.feature import Feature

    def x(session):
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
                extraneous_names.remove(name.upper())
                    
            for name in extraneous_names:
                del name_to_feature[name]
                 
            return name_to_feature
        else:
            return {}
    return x
