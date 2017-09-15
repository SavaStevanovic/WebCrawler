'''
Searches web page and adds data to database,
and queue for further processing

Created on Sep 9, 2017
@author: Sava
'''
import sys
import requests
import multiprocessing
import DBClasses
from bs4 import BeautifulSoup 
from sqlalchemy import create_engine, MetaData, Table

def extractLinkParts(linkQuery):
        linkParts = linkQuery.split('?')
        if(len(linkParts) > 1):
            return (linkParts[0], [{'name':par.split('=')[0], 'value':par.split('=')[1]} for par in linkParts[1].split('&')])
        return (linkQuery, [])

class ScraperProcess(multiprocessing.Process):
    '''
    A single process of web crawler
    '''
    
    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()


    def __init__(self, baseLink, queue, restricter, procesed_set):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.restricter = restricter
        self.queue = queue
        self.baseLink = baseLink
        self.procesed_set = procesed_set
    

    def linkBackslashReducer(self, href):
        if (self.baseLink not in href):
            href = (self.baseLink + href).replace('///', '//').replace('///', '//')
        return href

    def run(self):  
        engine = create_engine(DBClasses.databaseLocation)   
        metadata = MetaData(bind=engine)
        
        while not self.exit.is_set():
            idHtml, seed = self.queue.get()
            print(" seed:" + seed)
            try:
                html = requests.get(seed)
                htmlTable = Table(DBClasses.tableHtml, metadata, autoload=True)
                updateStm = htmlTable.update().values(textValue=html.text.encode(sys.stdout.encoding, errors='replace')).where(htmlTable.columns.id == idHtml)
                engine.execute(updateStm)
            except Exception as e:
                print('    Error-Html processing:' + str(e))
                continue
            pritty_html = BeautifulSoup(html.text.encode(sys.stdout.encoding, errors='replace'), 'html.parser')
            for link in pritty_html.find_all('a'):
                try:
                    href = link.get('href')
                    if(href != None and any(link_part in href for link_part in self.restricter)):
                        href = self.linkBackslashReducer(href)
                        if(href not in self.procesed_set):
                            print(href) 
                            htmlTable = Table(DBClasses.tableHtml, metadata, autoload=True)
                            insertedHtml = engine.execute(htmlTable.insert().values(linkValue=href))
                            connTable = Table(DBClasses.tableConn, metadata, autoload=True)
                            engine.execute(connTable.insert().values(htmlSource=idHtml, htmlProduct=insertedHtml.inserted_primary_key[0]))
                            self.queue.put((insertedHtml.inserted_primary_key[0], href))  
                            self.procesed_set.append(href)
                       
                except Exception as e:
                    print('    Error-Html POSTprocessing:' + str(e))
            print(' ------' + str(len(self.procesed_set)) + " " + str(self.queue.qsize()))        
