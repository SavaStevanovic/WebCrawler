'''
Created on Sep 10, 2017

@author: Sava
'''

from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql import table, column, select, update, insert
from sqlalchemy.dialects.sqlite import \
            BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
            INTEGER, NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, \
            VARCHAR
Base = declarative_base()
engine = create_engine('sqlite:///WBDatabase.db')   
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData(bind=engine)

class Link(Base):
    '''
    classdocs
    '''
    __tablename__ = 'link'
        
    id = Column(Integer, primary_key=True)
    value = Column(String)
    
class Parameter(Base):
    '''
    classdocs
    '''
    __tablename__ = 'parameter'
        
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    link_id = Column(Integer, ForeignKey('link.id'))
    html_id = Column(Integer, ForeignKey('html.id'))
    
class Html(Base):
    '''
    classdocs
    '''
    __tablename__ = 'html'
        
    id = Column(Integer, primary_key=True)
    value = Column(String)

def getEngine():
    return engine

def sessionGetter(tableName):
        table = Table(tableName, metadata, autoload=True)
        s = table.select()
        result = session.execute(s)
        out = result.fetchall()
        print(out)
    
