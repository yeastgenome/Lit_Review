
from modelOldSchema.config import DBUSER, DBPASS
from modelOldSchema.model import Model, get_first
from queries.associate import associate
from queries.misc import get_feature_by_name, get_reftemps, validate_genes
from queries.move_ref import move_refbad_to_reftemp, move_reftemp_to_refbad, \
    move_reftemp_to_ref, move_ref_to_reftemp
from queries.parse import Task, TaskType
from unittest.suite import TestSuite
import unittest

class TestConnection(unittest.TestCase):
    
    def test_is_connected(self):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        self.assertTrue(conn.is_connected())
        

class TestGetAndMoveFeaturesAndReferences(unittest.TestCase):
        
    def test_get_feature_by_name_basic(self, feature_name='YJL001W', feature_id=1971):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        f = conn.execute(get_feature_by_name(feature_name))
        self.assertEqual(f.id, feature_id)
        
    def test_get_feature_by_name_case(self):
        feature_name = 'yjl001W'
        feature_id = 1971
        self.test_get_feature_by_name_basic(feature_name, feature_id)
        
    def test_get_feature_by_name_genename(self):
        gene_name = 'PRE3'
        feature_id = 1971
        self.test_get_feature_by_name_basic(gene_name, feature_id)
    
    def test_get_reftemp_by_pmid(self, pubmed_id=23125886, reftemp_id=81007):
        self.valid_reftemp(pubmed_id, reftemp_id)
    
    def test_get_refbad_by_pmid(self, pubmed_id=16998476):
        self.valid_refbad(pubmed_id)
    
    def test_get_ref_by_pmid(self, pubmed_id=1986222, ref_id=84):
        self.valid_ref(pubmed_id, ref_id)
        
    def test_get_reftemps(self):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        rs = conn.execute(get_reftemps())
        self.assertTrue(len(rs) > 0)
        
    def test_move_refbad_to_reftemp(self, pubmed_id=16830189):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        try:
            result = conn.execute(move_refbad_to_reftemp(pubmed_id))
            self.assertTrue(result)
            self.valid_reftemp(pubmed_id)
        finally:
            conn.execute(move_reftemp_to_refbad(pubmed_id))
        
    def test_move_reftemp_to_refbad(self, pubmed_id=23127840):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        try:
            result = conn.execute(move_reftemp_to_refbad(pubmed_id))
            self.assertTrue(result)
            self.valid_refbad(pubmed_id)
        finally:
            conn.execute(move_refbad_to_reftemp(pubmed_id))
        
    def test_move_reftemp_to_ref(self, pubmed_id=22830526):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        try:
            result = conn.execute(move_reftemp_to_ref(pubmed_id))
            self.assertTrue(result)
            self.valid_ref(pubmed_id)
        finally:
            conn.execute(move_ref_to_reftemp(pubmed_id))
            
    def test_move_ref_to_reftemp(self, pubmed_id=10085156):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        try:
            result = conn.execute(move_ref_to_reftemp(pubmed_id))
            self.assertTrue(result)
            self.valid_reftemp(pubmed_id)
        finally:
            conn.execute(move_reftemp_to_ref(pubmed_id))
            
    def valid_ref(self, pubmed_id, ref_id=None):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        
        from modelOldSchema.reference import Reference
        ref = conn.execute(lambda session: get_first(session, Reference, pubmed_id=pubmed_id))
        
        self.assertTrue(ref.abstract is not None)
        self.assertTrue(ref.journal is not None)
        self.assertTrue(ref.created_by is not None)
        self.assertTrue(ref.date_created is not None)
        
        self.assertEqual(ref.pubmed_id, pubmed_id)
        if ref_id is not None:
            self.assertEqual(ref.id, ref_id)
            
    def valid_reftemp(self, pubmed_id, reftemp_id=None):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        
        from modelOldSchema.reference import RefTemp
        reftemp = conn.execute(lambda session: get_first(session, RefTemp, pubmed_id=pubmed_id))
        
        self.assertTrue(reftemp.citation is not None)
        self.assertTrue(reftemp.abstract is not None)
        self.assertTrue(reftemp.created_by is not None)
        self.assertTrue(reftemp.date_created is not None)
        
        self.assertEqual(reftemp.pubmed_id, pubmed_id)
        if reftemp_id is not None:
            self.assertEqual(reftemp.id, reftemp_id)
            
    def valid_refbad(self, pubmed_id):
        conn = Model()
        conn.connect(DBUSER, DBPASS)
        
        from modelOldSchema.reference import RefBad
        refbad = conn.execute(lambda session: get_first(session, RefBad, pubmed_id=pubmed_id))
        
        self.assertTrue(refbad.created_by is not None)
        self.assertTrue(refbad.date_created is not None)
        
        self.assertEqual(refbad.pubmed_id, pubmed_id)
            
class TestAssociate(unittest.TestCase):
    
    def test_validate_genes(self):
        gene_names = ['YAL002W', 'CEN1', 'SPO7', 'YAL016C-B', 'YAL009W']
        feature_ids = [6102, 2899, 6347, 7398, 6347]

        conn = Model()
        conn.connect(DBUSER, DBPASS)
        name_to_feature = conn.execute(validate_genes(gene_names))
        
        self.assertEqual(len(gene_names), len(name_to_feature))
        for i in range(0, len(gene_names)):
            self.assertEqual(name_to_feature[gene_names[i]].id, feature_ids[i])
            
    def test_associate(self):
        pubmed_id = 23113558
        gene_names = ['ACT1', 'CEN1', 'SPO7', 'YAL016C-B', 'YAL009W']

        conn = Model()
        conn.connect(DBUSER, DBPASS)
        
        from modelOldSchema.reference import Reference

        try:
            conn.execute(move_reftemp_to_ref(pubmed_id))
            name_to_feature = conn.execute(validate_genes(gene_names))
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
            
            result = conn.execute(associate(pubmed_id, name_to_feature, tasks))
            self.assertTrue(result)
            
            
            curations = conn.execute(lambda session: get_first(session, Reference, pubmed_id=pubmed_id).curations)
            lit_guides = conn.execute(lambda session: get_first(session, Reference, pubmed_id=pubmed_id).litGuides)
            
            self.assertEqual(len(curations), 8)
            for curation in curations:
                self.assertTrue(curation.comment is not None)
                
                if curation.task == 'Gene Link':
                    self.assertTrue(False, 'The two Tasks with name Gene Link: ADD_TO_DATABASE and REVIEWS have no genes. They should not have curaitons.')
                   
            self.assertEqual(len(lit_guides), 3)
            for lit_guide in lit_guides:
                if curation.task == 'Reviews':
                    self.assertEqual(len(lit_guide.features), 0)
    
        finally:
            conn.execute(move_ref_to_reftemp(pubmed_id))

        
        
if __name__ == '__main__':
    suite = TestSuite()
    suite.addTest(TestAssociate('test_associate'))
    unittest.TextTestRunner().run(suite)
    