'''
Created on Sep 9, 2017

@author: Sava
'''
import sys
import requests
import multiprocessing
import DBClasses
from sqlalchemy.sql import table, column, select, update, insert
from bs4 import BeautifulSoup 
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql import table, column, select, update, insert

class ScraperProcess(multiprocessing.Process):
    '''
    classdocs
    '''
    @staticmethod
    def extractLinkParts(linkQuery):
        linkParts=linkQuery.split('?')
        if(len(linkParts)>1):
            return (linkParts[0],[{'name':par.split('=')[0],'value':par.split('=')[1]} for par in linkParts[1].split('&')])
        return (linkQuery,[])
    
    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()


    def __init__(self, baseLink, condition, queue, restricter, procesed_set):
        '''
        Constructor
        '''
        
        # self.dbsession=session
        # self.engine=engine
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.condition = condition
        self.restricter = restricter
        self.queue = queue
        self.baseLink = baseLink
        self.procesed_set = procesed_set
    
    def run(self):  
        engine = create_engine('sqlite:///WBDatabase.db')   
        # Session = sessionmaker(bind=engine)
        # session=Session()
        metadata = MetaData(bind=engine)
        
        while not self.exit.is_set():
            # print(seeds[index])
            idHtml,seed = self.queue.get()
            
            # self.engine.execute(DBClasses.getTable('link').insert(), value=seed)
            print("seed:" + seed)
            try:
                html = requests.get(seed)
                htmlTable=Table('html', metadata, autoload=True)
                updateStm=htmlTable.update().values(textValue=html.text.encode(sys.stdout.encoding, errors='replace')).where(htmlTable.columns.id==idHtml)
                engine.execute(updateStm)
                #insertedHtml = engine.execute(htmlTable.update().where(id=idHtml).values(textValue=html.text.encode(sys.stdout.encoding, errors='replace')))
            except Exception as e:
                print('~~~~~~Error~~~~~~')
                print(e)
                print('~~~~~~Error~~~~~~')
                continue
            pritty_html = BeautifulSoup(html.text.encode(sys.stdout.encoding, errors='replace'), 'html.parser')
            for link in pritty_html.find_all('a'):
                try:
                    href = link.get('href')
                    if(href!=None and any(link_part in href for link_part in self.restricter)):
                        if(self.baseLink not in href):
                                href = (self.baseLink + href).replace('///','//').replace('///','//')
                        if(href not in self.procesed_set):
                            print(href) 
                            htmlTable=Table('html', metadata, autoload=True)
                            insertedHtml = engine.execute(htmlTable.insert().values(linkValue=href))
                            
                            connTable = Table('conn', metadata, autoload=True)
                            engine.execute(connTable.insert().values(htmlSource=idHtml,htmlProduct=insertedHtml.inserted_primary_key[0]))
                            self.queue.put((insertedHtml.inserted_primary_key[0],href))  
                            self.procesed_set.append(href)
                       
                except Exception:
                    print('-1-1-1-1-1-1-1')
                    try:
                        print(Exception.args[0])
                    except: 
                        print(Exception)
            print('------' + str(len(self.procesed_set)) + " " + str(self.queue.qsize())
)      
            
        print(seed)   
        
