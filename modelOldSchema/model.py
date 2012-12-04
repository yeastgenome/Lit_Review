'''
Created on Oct 18, 2012

@author: kpaskov

This class is used to perform queries and operations on the corresponding database. In this case, the BUD schema on fasolt.

'''
from modelOldSchema import Base
from modelOldSchema.config import DBTYPE, DBHOST, DBNAME
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
import modelOldSchema
import sys
import traceback

# imports of model classes from model.feature, model.taxonomy, etc are done as needed, since these imports are
# not available until AFTER the metadata is bound to the engine.

class Model(object):
    '''
    This class acts as a divider between the Oracle back-end and the application. In order to pull information
    from the Oracle DB, this class MUST be called.
    '''
    engine = None
    SessionFactory = None
 
    def connect(self, username, password):
        """
        Create engine, associate metadata with the engine, then create a SessionFactory for use through the backend.
        """
        self.engine = create_engine("%s://%s:%s@%s/%s" % (DBTYPE, username, password, DBHOST, DBNAME), convert_unicode=True, pool_recycle=3600)
        Base.metadata.bind = self.engine
        self.SessionFactory = sessionmaker(bind=self.engine)
        modelOldSchema.current_user = username.upper()

        return
    
    def is_connected(self):
        #Checks if a connection to the db has been made.
        try:
            self.engine.connect()
            return True
        except:                 
            traceback.print_exc(file=sys.stdout)
            return False
        
    def execute(self, f, **kwargs):
        try:
            session = self.SessionFactory()
            return f(session, **kwargs)
        except:
            session.rollback()
            traceback.print_exc(file=sys.stdout)
            return False
        finally:
            session.close()

def get(session, model, **kwargs):
    instances = session.query(model).filter_by(**kwargs).all()
    return instances

def get_first(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    return instance

def create(session, model, **kwargs):
    return model(session=session, **kwargs)

def count(session, model, **kwargs):
    count = session.query(model).filter_by(**kwargs).count()
    return count
    
def get_or_create(session, model, **kwargs):
    instance = get_first(session, model, **kwargs)
    if instance:
        return instance
    else:
        instance = create(session, model, **kwargs)
    return instance
    
    