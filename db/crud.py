# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: crud.py 
@time: 2022/06/23
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""

from sqlalchemy.orm import Session
import db.models as models
import schemas
from mumu_exceptions import InsufficientAccessPermissionError, TagNotFoundError, ItemNotFoundError


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, name: str) -> models.User:
    return db.query(models.User).filter(models.User.name == name).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(name=user.name,
                          email=user.email,
                          hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, user_id: int) -> None:
    db_user = get_user_by_id(db, user_id)
    db.delete(db_user)
    db.commit()


def create_item(db: Session, item: schemas.ItemCreate, user: models.User) -> models.Item:
    db_item = models.Item(title=item.title,
                          content=item.content,
                          owner=user)
    db_item.tags = [read_tag(db, tag_id, user) for tag_id in item.linked_tag_ids]
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def read_item(db: Session, item_id: int, user: models.User) -> models.Item:
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise ItemNotFoundError
    if item.owner != user:
        raise InsufficientAccessPermissionError
    return item


def delete_item(db: Session, item_id: int, user: models.User) -> None:
    db_item = read_item(db, item_id, user)
    db.delete(db_item)
    db.commit()


def edit_item(db: Session, item_id: int, updated_item: schemas.ItemEdit, user: models.User) -> models.Item:
    """ 编辑项目
    """
    db_item = read_item(db, item_id, user)
    updated_item_dict = updated_item.dict(exclude_unset=True)
    for key, value in updated_item_dict.items():
        if key == 'linked_tag_ids':
            db_item.tags = [read_tag(db, tag_id, user) for tag_id in value]
        else:
            setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_tag(db: Session, tag: schemas.TagCreate, user: models.User) -> models.Tag:
    """ 创建一个标签
    """
    db_tag = models.Tag(title=tag.title,
                        content=tag.content,
                        owner=user)
    db_tag.parent_tag_id = tag.parent_tag_id
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def read_tag(db: Session, tag_id: int, user: models.User) -> models.Tag:
    """ 读取标签
    """
    tag: models.Tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag is None:
        raise TagNotFoundError
    if tag.owner != user:
        raise InsufficientAccessPermissionError
    return tag


def delete_tag(db: Session, tag_id: int, user: models.User) -> None:
    """ 删除标签
    """
    db_tag = read_tag(db, tag_id, user)
    db.delete(db_tag)
    db.commit()


def edit_tag(db: Session, tag_id: int, updated_tag: schemas.TagEdit, user: models.User) -> models.Tag:
    """ 编辑标签
    """
    db_tag = read_tag(db, tag_id, user)
    updated_tag_dict = updated_tag.dict(exclude_unset=True)
    for key, value in updated_tag_dict.items():
        setattr(db_tag, key, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def list_tags_of_target_user(db: Session, user: models.User) -> list[models.Tag]:
    """ 列出该用户的所有标签
    """
    return user.tags


def list_items_of_target_user(db: Session, user: models.User) -> list[models.Item]:
    """ 列出该用户的所有备忘事项
    """
    return user.items


def list_tags_of_target_item(db: Session,
                             item_id: int,
                             user: models.User) -> list[models.Tag]:
    """ 列出该备忘事项的所有标签
    """
    item = read_item(db, item_id, user)
    return item.tags


def list_items_of_target_tag(db: Session,
                             tag_id: int,
                             user: models.User) -> list[models.Item]:
    tag = read_tag(db, tag_id, user)
    return tag.items
