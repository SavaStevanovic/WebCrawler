'''
Created on Sep 9, 2017

@author: Sava
'''
#Start http://www.pmf.ni.ac.rs/pmf/index.php pmf
#Start https://www.wikipedia.org/ wikipe
#Stop

from WebCrowler import WebCrowler
import time

def sss(webCrawler, command):
    commandParts = [part.strip(' ') for part in command.split(' ')]
    if (commandParts[0] == 'Start'):
        if (webCrawler != None):
            webCrawler.processesShutDown()
        webCrawler = WebCrowler(commandParts[1], commandParts[2].split(','))
        webCrawler.processesEngage()
    if (commandParts[0] == 'Stop'):
        if (webCrawler != None):
            webCrawler.processesShutDown()
    return webCrawler


if __name__ == '__main__':
    started=True
    webCrawler=None
    while started:
        try:
            command=input(">:");
            webCrawler = sss(webCrawler, command)
            print('Program started.')
            time.sleep(0.5)
        except KeyboardInterrupt:  
            if(webCrawler!=None):
                webCrawler.processesShutDown()
        
        
