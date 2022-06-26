# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: constants.py 
@time: 2022/06/24
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""

# to get a string like this run:
# openssl rand -hex 32
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
