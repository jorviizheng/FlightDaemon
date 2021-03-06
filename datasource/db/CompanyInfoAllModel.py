from sqlalchemy import Column
from sqlalchemy.types import * #@UnusedWildImport
from sqlalchemy import and_ #@UnusedImport
import datetime
import DBBase


class CompanyInfoAll(DBBase.Base):
    __tablename__ = 'company_info_all_table'
    company_short = Column(VARCHAR(50), primary_key = True, index = True)  
    company_zh = Column(VARCHAR(100))
    company_en = Column(VARCHAR(100))
    state = Column(VARCHAR(100))
    date = Column(VARCHAR(20))
       
    
    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
           
            
    @staticmethod    
    def find(**kwargs):
        session = DBBase.getSession()
        key_item = session.query(CompanyInfoAll).filter_by(**kwargs).all()
        DBBase.Session.remove()
        return key_item
        

    def add(self):
        session = DBBase.getSession()
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.add(self)
        session.commit()
        DBBase.Session.remove()
    
    
    def delete(self):
        session = DBBase.getSession()
        ret = self.find()
        if ret is not None:
            session.delete(ret)
        session.commit()
        DBBase.Session.remove()
        

    
        
        
