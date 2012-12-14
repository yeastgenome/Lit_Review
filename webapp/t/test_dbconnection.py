
from modelOldSchema.config import DBUSER, DBPASS
from modelOldSchema.model import Model, get_first
from queries.associate import associate
from queries.misc import get_feature_by_name, get_reftemps, validate_genes
from queries.move_ref import move_refbad_to_reftemp, move_reftemp_to_refbad, \
    move_reftemp_to_ref, move_ref_to_reftemp
from queries.parse import Task, TaskType
from unittest.suite import TestSuite
import unittest

class ModelCreationMixin(unittest.TestCase):
    def setUp(self):
        self.model = Model()
        self.model.connect(DBUSER, DBPASS)

class TestConnection(ModelCreationMixin):
    
    def test_is_connected(self):
        self.assertTrue(self.model.is_connected())


class TestGetAndMoveFeaturesAndReferences(ModelCreationMixin):
        
    def test_get_feature_by_name(self, feature_name='YJL001W', feature_id=1971):
        f = self.model.execute(get_feature_by_name(feature_name))
        self.assertEqual(f.id, feature_id)
        
    def test_get_feature_by_name_case(self, feature_name='yjl001W', feature_id=1971):
        self.test_get_feature_by_name(feature_name, feature_id)
        
    def test_get_feature_by_name_genename(self, gene_name='PRE3', feature_id=1971):
        self.test_get_feature_by_name(feature_name=gene_name)
    
    def test_get_reftemp_by_pmid(self, pubmed_id=23125886, reftemp_id=81007):
        self.model.execute(self.valid_reftemp(pubmed_id, reftemp_id))
    
    def test_get_refbad_by_pmid(self, pubmed_id=16998476):
        self.model.execute(self.valid_refbad(pubmed_id))
    
    def test_get_ref_by_pmid(self, pubmed_id=1986222, ref_id=84):
        self.model.execute(self.valid_ref(pubmed_id, ref_id))
        
    def test_get_reftemps(self):
        rs = self.model.execute(get_reftemps())
        self.assertTrue(len(rs) > 0)
        
    def test_move_refbad_to_reftemp(self, pubmed_id=16830189):
        def f(session):    
            result = move_refbad_to_reftemp(pubmed_id, session)  
            self.assertTrue(result)
            self.valid_reftemp(pubmed_id, session=session)
            move_reftemp_to_refbad(pubmed_id, session) 
        
        self.model.execute(f)

    def test_move_reftemp_to_refbad(self, pubmed_id=23220089):
        def f(session):
            result = move_reftemp_to_refbad(pubmed_id, session)
            self.assertTrue(result)
            self.valid_refbad(pubmed_id, session=session)
            move_refbad_to_reftemp(pubmed_id, session)
            
        self.model.execute(f)

    def test_move_reftemp_to_ref(self, pubmed_id=23117410):
        def f(session):
            result = move_reftemp_to_ref(pubmed_id, session)
            self.assertTrue(result)
            self.valid_ref(pubmed_id, session=session)
            move_ref_to_reftemp(pubmed_id, session)
            
        self.model.execute(f)
  
    def test_move_ref_to_reftemp(self, pubmed_id=7962081):
        def f(session):
            result = move_ref_to_reftemp(pubmed_id, session)
            self.assertTrue(result)
            self.valid_reftemp(pubmed_id, session=session)
            move_reftemp_to_ref(pubmed_id, session)
            
        self.model.execute(f)
            
    def valid_ref(self, pubmed_id, ref_id=None, session=None):
        def f(session):
            from modelOldSchema.reference import Reference
            ref = get_first(Reference, session=session, pubmed_id=pubmed_id)
        
            self.assertTrue(ref.abstract is not None)
            self.assertTrue(ref.journal is not None)
            self.assertTrue(ref.created_by is not None)
            self.assertTrue(ref.date_created is not None)
        
            self.assertEqual(ref.pubmed_id, pubmed_id)
            if ref_id is not None:
                self.assertEqual(ref.id, ref_id)
        return f if session is None else f(session)
 
    def valid_reftemp(self, pubmed_id, reftemp_id=None, session=None):
        def f(session):
            from modelOldSchema.reference import RefTemp
            reftemp = get_first(RefTemp, session=session, pubmed_id=pubmed_id)
        
            self.assertTrue(reftemp.citation is not None)
            self.assertTrue(reftemp.abstract is not None)
            self.assertTrue(reftemp.created_by is not None)
            self.assertTrue(reftemp.date_created is not None)
        
            self.assertEqual(reftemp.pubmed_id, pubmed_id)
            if reftemp_id is not None:
                self.assertEqual(reftemp.id, reftemp_id)
        return f if session is None else f(session)
            
    def valid_refbad(self, pubmed_id, session=None):    
        def f(session):
            from modelOldSchema.reference import RefBad
            refbad = get_first(RefBad, session=session, pubmed_id=pubmed_id)
        
            self.assertTrue(refbad.created_by is not None)
            self.assertTrue(refbad.date_created is not None)
        
            self.assertEqual(refbad.pubmed_id, pubmed_id)
        return f if session is None else f(session)
            
class TestAssociate(ModelCreationMixin):
    
    def test_validate_genes(self):
        gene_names = ['YAL002W', 'CEN1', 'SPO7', 'YAL016C-B', 'YAL009W']
        feature_ids = [6102, 2899, 6347, 7398, 6347]

        name_to_feature = self.model.execute(validate_genes(gene_names))
        
        self.assertEqual(len(gene_names), len(name_to_feature))
        for i in range(0, len(gene_names)):
            self.assertEqual(name_to_feature[gene_names[i]].id, feature_ids[i])
            
    def test_associate(self):
        def f(session):
            pubmed_id = 23222539
            gene_names = ['ACT1', 'CEN1', 'SPO7', 'YAL016C-B', 'YAL009W']
        
            from modelOldSchema.reference import Reference

            move_reftemp_to_ref(pubmed_id, session=session)
            name_to_feature = self.model.execute(validate_genes(gene_names))
            tasks = [Task(TaskType.HIGH_PRIORITY, None, "Comment"),
                     Task(TaskType.DELAY, None, "Comment"),
                     Task(TaskType.HTP_PHENOTYPE_DATA, None, "Comment"),
                     Task(TaskType.OTHER_HTP_DATA, None, "Comment"),
                     
                     Task(TaskType.CLASSICAL_PHENOTYPE_INFORMATION, ['ACT1'], "Comment"),
                     Task(TaskType.GO_INFORMATION, ['ACT1'], "Comment"),
                     Task(TaskType.HEADLINE_INFORMATION, ['YAL009W', 'YAL016C-B'], "Comment"),
                     
                     Task(TaskType.ADD_TO_DATABASE, None, "Comment"),
                     Task(TaskType.REVIEWS, None, "Comment")
                     ]
            
            result = associate(pubmed_id, name_to_feature, tasks, session=session)
            self.assertTrue(result)
            
            
            curations = get_first(Reference, session=session, pubmed_id=pubmed_id).curations
            lit_guides = get_first(Reference, session=session, pubmed_id=pubmed_id).litGuides
            
            self.assertEqual(len(curations), 8)
            for curation in curations:
                self.assertTrue(curation.comment is not None)
                
                if curation.task == 'Gene Link':
                    self.assertTrue(False, 'The two Tasks with name Gene Link: ADD_TO_DATABASE and REVIEWS have no genes. They should not have curaitons.')
                   
            self.assertEqual(len(lit_guides), 3)
            for lit_guide in lit_guides:
                if curation.task == 'Reviews':
                    self.assertEqual(len(lit_guide.features), 0)
    
            move_ref_to_reftemp(pubmed_id, session=session)
        self.model.execute(f)

        
        
if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestGetAndMoveFeaturesAndReferences('test_get_feature_by_name_genename'))
    unittest.TextTestRunner().run(suite)
    
