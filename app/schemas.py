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

import datetime

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
    id: int = Field(
        description="备忘事项的唯一标识符id"
    )
    tags: list['TagOutline'] = Field(
        default=[],
        description="标签概要列表, 元素为(标签id, 标签标题)"
    )

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    linked_tag_ids: list[int] = Field(
        default=[],
        description="关联的标签id列表"
    )


class ItemEdit(ItemCreate):
    pass


class ItemOutline(BaseModel):
    id: int = Field(
        description="备忘事项的唯一标识符id"
    )
    title: str | None = Field(
        default=None,
        description="备忘事项的标题",
        max_length=100
    )

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    title: str = Field(
        default="未命名标签",
        title="标签标题",
        max_length=100
    )
    content: str | None = Field(
        default=None,
        description="标签的详细内容",
    )


class TagCreate(TagBase):
    parent_tag_id: int | None = Field(
        default=None,
        description="父标签id"
    )


class TagEdit(TagCreate):
    pass


class TagOutline(BaseModel):
    id: int = Field(
        description="标签的唯一标识符id"
    )
    title: str | None = Field(
        default=None,
        description="标签的标题",
        max_length=100
    )

    class Config:
        orm_mode = True


class Tag(TagBase):
    id: int = Field(
        description="标签的唯一标识符id"
    )
    parent_tag: TagOutline | None = Field(
        default=None,
        description="父标签的概要信息"
    )
    child_tags: list['TagOutline'] = Field(
        default=[],
        description="子标签的概要信息列表, 元素为(标签id, 标签标题)"
    )
    items: list['ItemOutline'] = Field(
        default=[],
        description="关联的备忘事项的概要信息列表, 元素为(备忘事项id, 备忘事项标题)"
    )

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str = Field(
        default="未命名用户",
        title="用户名",
        max_length=100
    )
    email: str | None = Field(
        default=None,
        description="用户的邮箱"
    )


class UserCreate(UserBase):
    password: str = Field(
        description="用户的密码"
    )


class User(UserBase):
    id: int = Field(
        description="用户的唯一标识符id"
    )
    items: list[ItemOutline] = Field(
        default=[],
        description="用户的备忘事项的概要信息列表, 元素为(备忘事项id, 备忘事项标题)"
    )
    tags: list[TagOutline] = Field(
        default=[],
        description="用户的标签的概要信息列表, 元素为(标签id, 标签标题)"
    )

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str = Field(
        description="访问令牌"
    )
    token_type: str = Field(
        description="令牌类型"
    )
    token_expires: datetime.datetime = Field(
        description="令牌过期时间"
    )


class TokenData(BaseModel):
    username: str | None = Field(
        default=None,
        description="用户名"
    )


# 由于Item引用了后面的TagOutline, 需要更新一下引用
Item.update_forward_refs()
