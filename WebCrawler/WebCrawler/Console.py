'''
Console for entering commands 

Created on Sep 9, 2017
@author: Sava
'''
# Start http://www.pmf.ni.ac.rs/pmf/index.php pmf
# Start https://www.wikipedia.org/ wikipe
# Stop

from WebCrawler import WebCrawler

def executeCommand(webCrawler, command):
    commandParts = [part.strip(' ') for part in command.split(' ')]
    if (commandParts[0] == 'Start'):
        if (webCrawler != None):
            webCrawler.processesShutDown()
        webCrawler = WebCrawler(commandParts[1], commandParts[2].split(','))
        webCrawler.processesEngage()
    if (commandParts[0] == 'Stop'):
        if (webCrawler != None):
            webCrawler.processesShutDown()
    return webCrawler

if __name__ == '__main__':
    started = True
    webCrawler = None
    while started:
        command = input(">:");
        webCrawler = executeCommand(webCrawler, command)
        print('Command executed')