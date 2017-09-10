'''
Created on Sep 10, 2017

@author: Sava
'''
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import \
            BLOB, BOOLEAN, CHAR, DATE, DATETIME, DECIMAL, FLOAT, \
            INTEGER, NUMERIC, SMALLINT, TEXT, TIME, TIMESTAMP, \
            VARCHAR
import DBClasses     
       


class WBDatabase(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

        engine = create_engine('sqlite:///WBDatabase.db')
        conn = engine.connect()
