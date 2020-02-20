#!/usr/bin/python
####################################
# Created by Max Aaronson
# 3/26/18
####################################

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import jsonify
from werkzeug.security import check_password_hash
from flask_login import UserMixin

Base = declarative_base()


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(80))
    type = Column(String(80))
    description = Column(String(500))
    github_link = Column(String(150))
    link2 = Column(String(150))
    link2_txt = Column(String(80))
    link3 = Column(String(150))
    link3_txt = Column(String(80))

class Education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200))
    school = Column(String(200))
    extra_column = Column(String())

class Work_Experience(Base):
    __tablename__ = 'work_experience'
    id = Column(Integer, primary_key=True, nullable=False)
    company = Column(String(200))
    job_title = Column(String(200))
    extra_column = Column(String())

class About(Base):
    __tablename__ = 'about'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(80))
    description = Column(String(1000))

class User(UserMixin, Base):
    __tablename__ = "user"     
    id = Column(Integer, primary_key=True)  
    user_name = Column(String(64))
    user_pass = Column(String(128))

    # is_authenticated = True

    def checkPassword(self, form_data):
        #print ("result is ")
        #print(check_password_hash(self.user_pass, form_data))
        return check_password_hash(self.user_pass, form_data)        

    def __repr__(self):
        return self.user_name
                                            
engine = create_engine(open('/home/amset/webapps/max_flask/htdocs/db_connect').readline())

Base.metadata.create_all(engine)
