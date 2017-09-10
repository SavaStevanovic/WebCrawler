'''
Created on Sep 9, 2017

@author: Sava
'''
import sys
import requests
import multiprocessing
from bs4 import BeautifulSoup 

class ScraperProcess(multiprocessing.Process):
    '''
    classdocs
    '''

    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()


    def __init__(self, baseLink, condition, queue, restricter, procesed_set):
        '''
        Constructor
        '''
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.condition = condition
        self.restricter=restricter
        self.queue=queue
        self.baseLink=baseLink
        self.procesed_set=procesed_set
    
    def run(self):  
        while not self.exit.is_set():
            #print(seeds[index])
            seed=self.queue.get()
            print("seed:"+seed)
            try:
                html=requests.get(seed)
            except Exception as e:
                print('~~~~~~Error~~~~~~')
                print(e)
                print('~~~~~~Error~~~~~~')
                continue
            pritty_html=BeautifulSoup(html.text.encode(sys.stdout.encoding, errors='replace'),'html.parser')
            for link in pritty_html.find_all('a'):
                try:
                    href=link.get('href')
                    if(any(link_part in href for link_part in self.restricter)):
                        if(self.baseLink not in href):
                                href=self.baseLink+href
                        if(href not in self.procesed_set):
                            print(href) 
                            self.queue.put(href)  
                            self.procesed_set.append(href)
                except Exception:
                    print('-1-1-1-1-1-1-1')
                    #print(pritty_html.find_all('a'))
                    print(Exception.args[0])
            print('------'+str(len(self.procesed_set))+" "+str(self.queue.qsize())
)      
            
        print(seed)   
        