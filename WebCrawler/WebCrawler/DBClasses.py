'''
Database used to store web pages and their links

Created on Sep 10, 2017
@author: Sava
'''

from sqlalchemy import create_engine, MetaData, Table, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.sql import table
from sqlalchemy.dialects.sqlite import  TEXT

# constants
tableHtml = 'html'
tableConn = 'conn'
tableHtmlId = tableHtml + '.id'
databaseLocation = 'sqlite:///WBDatabase.db'

# module init
Base = declarative_base()
engine = create_engine(databaseLocation)   
metadata = MetaData(bind=engine)
    
class WebPage(Base):
    '''
    First argument is id of database row.
    Second argument is link which returns 
    html represented by third argument.
    '''
    __tablename__ = tableHtml
        
    id = Column(Integer, primary_key=True)
    linkValue = Column(TEXT)
    textValue = Column(TEXT)
    
class Connection(Base):
    '''
    First parameter is id of a page which contains link 
    to page with id represented with second parameter.
    '''
    __tablename__ = tableConn
        
    htmlSource = Column(Integer, ForeignKey(tableHtmlId), primary_key=True)
    htmlProduct = Column(Integer, ForeignKey(tableHtmlId), primary_key=True)
    
    __table_args__ = (ForeignKeyConstraint([htmlSource, htmlProduct],
                                           [WebPage.id, WebPage.id]),
                      {})
    
# creates database tables if not already created.
def initiateDatabase():
    Base.metadata.create_all(engine)

# initiates database by adding link if not present in database. Returns id of link in database.        
def initiateLinkSearch(link):
    table = Table(tableHtml, metadata, autoload=True)
    s = engine.execute(table.select().where(table.columns.linkValue == link))
    links = s.fetchall()
    if(len(links) == 0):
        insertedHtml = engine.execute(table.insert().values(linkValue=link)).inserted_primary_key[0]
    else:
        insertedHtml = links[0].id
    return insertedHtml, link

# returns all unprocessed links.
def getHtmlQueueForProcessing():
    html = Table(tableHtml, metadata, autoload=True)
    links = engine.execute(html.select().where(html.columns.textValue == None)).fetchall()
    return [(entry.id, entry.linkValue) for entry in links]

# returns all found links.
def getEnteredHtmlSet():
    table = Table(tableHtml, metadata, autoload=True)
    s = engine.execute(table.select())
    links = s.fetchall()
    return [entry.linkValue for entry in links]

# print entries of each table in database.
def databaseOutput(count=10):
    tables = engine.table_names()
    for tableName in tables:
        table = Table(tableName, metadata, autoload=True)
        tableOutput = engine.execute(table.select().limit(count)).fetchall()
        print(tableOutput)
    
