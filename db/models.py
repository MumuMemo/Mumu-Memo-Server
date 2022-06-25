# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: schemas.py
@time: 2022/06/19
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from db.base import Base, SessionLocal
from mumu_enums import ItemState


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    items = relationship(
        "Item", back_populates="owner",
        cascade="all, delete, delete-orphan",
        order_by="Item.id"
    )

    tags = relationship(
        "Tag",
        back_populates="owner",
        cascade="all, delete, delete-orphan",
        order_by="Tag.id"
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    state = Column(Enum(ItemState), default=ItemState.TODO, nullable=True)

    create_timestamp = Column(DateTime, nullable=True)
    last_updated_timestamp = Column(DateTime, nullable=True)
    finished_timestamp = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="items")
    tags = relationship("Tag", secondary="item_tags", back_populates="items")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)

    parent_tag_id = Column(
        Integer,
        ForeignKey('tags.id')
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    parent_tag = relationship(
        "Tag",
        remote_side=[id]
    )
    child_tags = relationship(
        "Tag",
        back_populates="parent_tag",
        cascade="all, delete, delete-orphan"
    )

    owner = relationship("User", back_populates="tags")
    items = relationship("Item", secondary="item_tags", back_populates="tags")


class ItemTag(Base):
    __tablename__ = "item_tags"

    item_id = Column(
        Integer,
        ForeignKey("items.id"),
        primary_key=True
    )
    tag_id = Column(
        Integer,
        ForeignKey("tags.id"),
        primary_key=True
    )


if __name__ == '__main__':
    import os
    import datetime

    if os.path.exists("sql_app.db"):
        os.remove("sql_app.db")
    # ONLY FOR TEST
    from db import engine

    session = SessionLocal()
    Base.metadata.create_all(bind=engine)
    test_user = User(email="jeza@vip.qq.com",
                     hashed_password="xxxx",
                     name="Jeza Chen")
    session.add(test_user)
    session.commit()
