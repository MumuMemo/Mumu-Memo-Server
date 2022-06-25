# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: depends.py 
@time: 2022/06/24
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 与用户鉴权的依赖项相关
"""
from __future__ import annotations

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from db import get_db

from schemas import TokenData

from db.crud import get_user_by_name, create_user
from users.constants import SECRET_KEY, ALGORITHM

__all__ = ["oauth2_scheme", "get_current_user"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 使用SECRET_KEY解密得到payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_name(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
