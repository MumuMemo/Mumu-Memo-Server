# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: base.py 
@time: 2022/06/19
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
