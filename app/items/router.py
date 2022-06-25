# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: router.py 
@time: 2022/06/19
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from db.models import User
from schemas import Item, ItemCreate, Tag, ItemEdit
from users.depends import get_current_user
import db.crud as db_crud

router = APIRouter(
    prefix='/items',
    tags=['items'],
    responses={
        404: {
            'description': 'Item not found.'
        }
    }
)


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    db_item = db_crud.read_item(db, item_id, user)
    return Item.from_orm(db_item)


@router.put("/", status_code=201, response_model=Item)
async def create_item(item: ItemCreate,
                      user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    db_item = db_crud.create_item(db, item, user)
    return db_item


@router.post("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemEdit,
                      user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    db_item = db_crud.edit_item(db, item_id, item, user)
    return db_item


@router.patch("/{item_id}", response_model=Item)
async def patch_item(item_id: int, item: ItemEdit,
                     user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    db_item = db_crud.edit_item(db, item_id, item, user)
    return db_item


@router.delete("/{item_id}", response_model=Item)
async def delete_item(item_id: int,
                      user: User = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    db_crud.delete_item(db, item_id, user)


@router.get("", response_model=list[Item])
async def list_items(user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    return db_crud.list_items_of_target_user(db, user)


@router.get("/{item_id}/tags", response_model=list[Tag])
async def list_tags_of_target_item(item_id: int,
                                   user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    """ 获取备忘事项的所有tag信息
    """
    return db_crud.list_tags_of_target_item(db, item_id, user)
