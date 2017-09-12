'''
Created on Sep 9, 2017

@author: Sava
'''
#Start http://www.pmf.ni.ac.rs/pmf/index.php pmf
#Start https://www.wikipedia.org/ wikipe

started=True;
from WebCrowler import WebCrowler
import time



def processCommand(command):
    commandParts=[part.strip(' ') for part in command.split(' ')]
    val={
        'Start':WebCrowler(commandParts[1],commandParts[2].split(',')).processesEngage(),
        #'Stop':WebCrowler(commandParts[1]).processesShutDown()
        }['Start']
    
    

if __name__ == '__main__':
    while started:
        try:
            command=input(">:");
            processCommand(command)
            print('Program started.')
            time.sleep(0.5)
        except KeyboardInterrupt:  
            started=False
        
        
