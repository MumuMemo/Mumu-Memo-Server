# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: schemas.py
@time: 2022/06/17
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from mumu_enums import ItemState


class ItemBase(BaseModel):
    """Base model for all items
    """
    title: str | None = Field(
        default=None,
        description="备忘事项的标题",
        max_length=100
    )
    content: str | None = Field(
        default=None,
        description="备忘事项的内容",
    )
    remind_timestamp: int | None = Field(
        default=None,
        description="提醒时间"
    )
    remind_interval: int | None = Field(
        default=None,
        description="提醒时间间隔, 下一次提醒时间 = 提醒时间 + 间隔"
    )

    create_timestamp: int | None = Field(
        default=None,
        description="备忘事项的创建时间"
    )
    last_updated_timestamp: int | None = Field(
        default=None,
        description="最近一次更新时间"
    )
    finished_timestamp: int | None = Field(
        default=None,
        description="备忘事项的完成时间"
    )
    state: ItemState = Field(
        default=ItemState.TODO,
        description="备忘事项的状态"
    )


class Item(ItemBase):
    """ Item model returned by the API
    """
    id: int
    tags: list['TagOutline'] = []  # 标签id, 标签标题

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    linked_tag_ids: list[int] = []  # 标签id


class ItemEdit(ItemCreate):
    pass


class ItemOutline(BaseModel):
    id: int
    title: str | None

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    title: str = Field(
        default="未命名标签",
        title="标签标题"
    )
    content: str | None = None


class TagCreate(TagBase):
    parent_tag_id: int | None = None  # 父标签id


class TagEdit(TagCreate):
    pass


class TagOutline(BaseModel):
    id: int
    title: str | None

    class Config:
        orm_mode = True


class Tag(TagBase):
    id: int
    parent_tag: TagOutline | None = None
    child_tags: list['TagOutline'] = []
    items: list['ItemOutline'] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    items: list[ItemOutline] = []
    tags: list[TagOutline] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# 由于Item引用了后面的TagOutline, 需要更新一下引用
Item.update_forward_refs()
