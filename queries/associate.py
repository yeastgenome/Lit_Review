'''
Created on Dec 4, 2012

@author: kpaskov
'''
from modelOldSchema.model import get_or_create, get_first
from queries.parse import TaskType

def associate(pubmed_id, name_to_feature, tasks):
    """
    Associate a Reference with LitGuide entries.
    """          
    
    from modelOldSchema.reference import Reference, RefCuration, LitGuide
              
    def x(session):
        reference = get_first(session, Reference, pubmed_id=pubmed_id)
   
        for task in tasks:     
            gene_names = task.gene_names
            if gene_names is not None and len(gene_names) > 0:
                #Convert gene_names to features using the name_to_feature table.                
                features = set()
                for gene_name in task.gene_names:
                    features.add(name_to_feature[gene_name.upper()])
                        
                ## Create RefCuration objects and add them to the Reference.
                for feature in features:
                    curation = get_or_create(session, RefCuration, reference_id = reference.id, task = task.name, feature_id = feature.id)
                    curation.comment = task.comment
                    reference.curations.append(curation)
                                
                ## Create a LitGuide object and attach features to it.
                lit_guide = get_or_create(session, LitGuide, topic=task.topic, reference_id = reference.id)
                for feature in features:
                    if not feature.id in lit_guide.feature_ids:
                        lit_guide.features.append(feature)
                reference.litGuides.append(lit_guide)
    
                        
            else:   ## no gene name provided
    
                ## if no gene name provided and "Add to database" was checked,
                ## no need to add any association
                if task.type == TaskType.ADD_TO_DATABASE:
                    continue
    
                ## if it is a review, no need to add to ref_curation
                if task.type == TaskType.REVIEWS:
                    ## topic = task = 'Reviews'
                    reference.litGuideTopics.append(task.topic)
                    continue
    
                curation = get_or_create(session, RefCuration, task=task.name, reference_id=reference.id, feature_id=None)
                curation.comment = task.comment
                reference.curations.append(curation)
                
                ## Create a LitGuide object.
                if task.type == TaskType.HTP_PHENOTYPE_DATA or task.type == TaskType.REVIEWS:
                    lit_guide = get_or_create(session, LitGuide, topic=task.topic, reference_id=reference.id)
                    reference.litGuides.append(lit_guide)
        
        session.commit()
          
        message = "RefCurations: "
        for curation in reference.curations:
            message = message + str(curation) + ", "
        message = message + "<p> LitGuides: "
        for lit_guide in reference.litGuides:
            message = message + str(lit_guide) + ", "
        return message
    return x
