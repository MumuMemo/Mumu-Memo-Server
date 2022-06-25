# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: test_app.py
@time: 2022/06/24
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import schemas
from db import Base
from db.crud import create_user


class TestDb(unittest.TestCase):
    def setUp(self) -> None:
        test_database_url = "sqlite://"

        engine = create_engine(
            test_database_url, connect_args={"check_same_thread": False}, echo=True
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session: Session = SessionLocal()
        Base.metadata.create_all(bind=engine)
        self.test_user = create_user(self.session,
                                     schemas.UserCreate(name="test", email="jeza@vip.qq.com", password="test"))

    def test_user_info(self):
        user = self.session.query(app.db.models.User).filter(app.db.models.User.id == self.test_user.id).first()
        self.assertEqual(user.name, "test")
        self.assertEqual(user.email, "jeza@vip.qq.com")
        self.assertEqual(user.hashed_password, "test")

    def tearDown(self) -> None:
        pass
