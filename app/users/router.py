# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: router.py 
@time: 2022/06/24
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""
from __future__ import annotations

from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

import schemas
from db import get_db
from schemas import Token
import hashlib
from db.crud import get_user_by_name, create_user
from users.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from users.depends import oauth2_scheme

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={
        404: {
            'description': 'User not found.'
        }
    }
)


def verify_password(password: str, hashed_password: str):
    return bytes.fromhex(hashed_password) == hashlib.sha256(password.encode()).digest()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_name(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    """  登录, 获取登录凭证
    """
    user = authenticate_user(db,
                             form_data.username,
                             form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token,
            "token_type": "bearer",
            "token_expires": access_token_expires + datetime.now()}


@router.post("/register", response_model=Token)
async def register_user(reg_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """  注册, 获取登录凭证
    """
    user = get_user_by_name(db, reg_data.name)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # 密码取哈希值来保存
    hashed_password = hashlib.sha256(reg_data.password.encode()).hexdigest()
    reg_data.password = hashed_password
    user = create_user(db, reg_data)
    if not user:
        raise HTTPException(status_code=400, detail="Something went wrong")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token,
            "token_type": "bearer",
            "token_expires": access_token_expires + datetime.now()}

