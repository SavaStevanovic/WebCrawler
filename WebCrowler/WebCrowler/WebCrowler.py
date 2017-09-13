'''
Created on Sep 9, 2017

@author: Sava
'''
from sqlalchemy import create_engine,inspect
import DBClasses
import multiprocessing
from ScraperProcess import ScraperProcess


class WebCrowler():
    '''
    classdocs
    '''
    
    def processesEngage(self):
        for p in self.processes:
            p.start();
    
    def processesShutDown(self):
        for p in self.processes:
            p.shutdown();
    
    @staticmethod
    def restrictorExtracter(seedLink):        
        linkParts=seedLink.split('://');
        partNum=len(linkParts)>1
        return list(linkParts[partNum].split('/')[0]);
    
    @staticmethod
    def baseLinkExtractor(seedLink):        
        linkParts=seedLink.split('://');
        partNum=len(linkParts)>1
        if partNum:
            return linkParts[0]+'://'
        return 'http://'

    def __init__(self, seedLink, restrictor=None):
        '''
        Constructor
        '''
        
        #self.dbsession=DBClasses.sessionGetter()
        DBClasses.initiateDatabase()
        DBClasses.databaseOutput()
        id,link=DBClasses.initiateLinkSearch(seedLink)
        self.restrictor=restrictor
        if(not restrictor):
            self.restrictor=self.restrictorExtracter(seedLink)
        self.queue=multiprocessing.Queue()
        toProcess=DBClasses.getProcessQueue()
        [self.queue.put(item) for item in toProcess]
        self.manager=multiprocessing.Manager()
        self.procesed_set=self.manager.list()
        [self.procesed_set.append(item) for item in DBClasses.getEnteredSet()]
        self.condition = multiprocessing.Condition();
        self.cpu_count=multiprocessing.cpu_count();
        self.base=self.baseLinkExtractor(seedLink)
        # base, condition, queue, restricter, procesed_set
        self.processes=[ScraperProcess(self.base,self.condition,self.queue,self.restrictor,self.procesed_set) for x in range(self.cpu_count)]
