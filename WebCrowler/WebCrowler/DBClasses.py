'''
Created on Sep 10, 2017

@author: Sava
'''

from sqlalchemy import create_engine, inspect, MetaData, Table, ForeignKeyConstraint
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
metadata = MetaData(bind=engine)
Base.metadata.create_all(engine)
    
class Html(Base):
    '''
    classdocs
    '''
    __tablename__ = 'html'
        
    id = Column(Integer, primary_key=True)
    linkValue = Column(TEXT)
    textValue = Column(TEXT)
    
class Connection(Base):
    '''
    classdocs
    '''
    __tablename__ = 'conn'
        
    htmlSource = Column(Integer, ForeignKey('html.id'), primary_key=True)
    htmlProduct = Column(Integer, ForeignKey('html.id'), primary_key=True)
    __table_args__ = (ForeignKeyConstraint([htmlSource, htmlProduct],
                                           [Html.id, Html.id]),
                      {})


def initiateDatabase():
    Base.metadata.create_all(engine)
        
def initiateLinkSearch(link):
    table = Table('html', metadata, autoload=True)
    s=engine.execute(table.select().where(table.columns.linkValue==link))
    links=s.fetchall()
    if(len(links)==0):
        insertedHtml = engine.execute(table.insert().values(linkValue=link)).inserted_primary_key[0]
    else:
        insertedHtml=links[0].id
    return insertedHtml,link

def databaseOutput():
    tables=engine.table_names()
    for tableName in tables:
        table = Table(tableName, metadata, autoload=True)
        s=engine.execute(table.select())
        out = s.fetchall()
        print(out)
    
