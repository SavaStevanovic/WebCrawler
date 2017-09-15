'''
Created on Sep 9, 2017

@author: Sava
'''
import DBClasses
import multiprocessing
from ScraperProcess import ScraperProcess

# not used in this implementation. Should split base link and parameters 
def restrictorExtracter(seedLink):        
    linkParts = seedLink.split('://');
    partNum = len(linkParts) > 1
    return list(linkParts[partNum].split('/')[0]);

# return http or https of seedLink
def baseLinkExtractor(seedLink):        
    linkParts = seedLink.split('://');
    partNum = len(linkParts) > 1
    if partNum:
        return linkParts[0] + '://'
    return 'http://'
    

class WebCrawler():
    '''
    Manages web crawler threads and enables queue loading from database
    '''
    
    def processesEngage(self):
        for p in self.processes:
            p.start();
    
    def processesShutDown(self):
        for p in self.processes:
            p.shutdown();
    

    def __init__(self, seedLink, restrictor=None):
        '''
        seedLink is initial link from which web crawler starts
        restrictor is string that must be part of link if it 
        should be processed so we can restrict which site is 
        stored in database
        '''
        DBClasses.initiateDatabase()
        DBClasses.databaseOutput()
        DBClasses.initiateLinkSearch(seedLink)
        if(not restrictor):
            self.restrictor = self.restrictorExtracter(seedLink)
        queue = multiprocessing.Queue()
        [queue.put(item) for item in DBClasses.getHtmlQueueForProcessing()]
        manager = multiprocessing.Manager()
        procesed_set = manager.list()
        [procesed_set.append(item) for item in DBClasses.getEnteredHtmlSet()]
        cpu_count = multiprocessing.cpu_count();
        base = baseLinkExtractor(seedLink)
        self.processes = [ScraperProcess(base, queue, restrictor, procesed_set) for _ in range(cpu_count)]
