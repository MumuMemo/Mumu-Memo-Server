# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: router.py 
@time: 2022/06/17
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from db.models import User
from schemas import Tag, TagCreate, Item, TagEdit
from users.depends import get_current_user
import db.crud as db_crud

router = APIRouter(
    prefix='/tags',
    tags=['tags'],
    responses={
        404: {
            'description': 'Tag not found.'
        }
    }
)


@router.get("/{tag_id}", response_model=Tag)
async def get_tag(tag_id: int,
                  user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    db_tag = db_crud.read_tag(db, tag_id, user)
    return Tag.from_orm(db_tag)


@router.put("/", status_code=201, response_model=Tag)
async def create_tag(tag: TagCreate,
                     user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    db_tag = db_crud.create_tag(db, tag, user)
    return db_tag


@router.post("/{tag_id}", response_model=Tag)
async def update_tag(tag_id: int,
                     tag: TagEdit,
                     user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    db_tag = db_crud.edit_tag(db, tag_id, tag, user)
    return db_tag


@router.patch("/{tag_id}", response_model=Tag)
async def patch_tag(tag_id: int,
                    tag: TagEdit,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    db_tag = db_crud.edit_tag(db, tag_id, tag, user)
    return db_tag


@router.delete("/{tag_id}")
async def delete_tag(tag_id: int,
                     user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    db_crud.delete_tag(db, tag_id, user)


@router.get("", response_model=list[Tag])
async def list_tags(user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """ 列出所有的标签
    """
    return db_crud.list_tags_of_target_user(db, user)


@router.get("/{tag_id}/items", response_model=list[Item])
async def list_items_of_target_tag(tag_id: int,
                                   user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    """ 获取指定tag的所有备忘事项
    """
    return db_crud.list_tags_of_target_item(db, tag_id, user)
