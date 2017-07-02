# -*- coding: utf-8 -*-
'''
Created on 27 june 2017
@author: pascal limeux
'''

from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
__db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = __db_session.query_property()

def drop_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def get_session():
    return __db_session

def init_db():
    Base.metadata.create_all(bind=engine)
