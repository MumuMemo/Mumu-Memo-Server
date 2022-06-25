# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: mumu_exceptions.py
@time: 2022/06/24
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""

from fastapi import status, FastAPI
from fastapi.responses import JSONResponse

__all__ = ["MumuException",
           "InsufficientAccessPermissionError",
           "TagNotFoundError",
           "ItemNotFoundError",
           "register_exception_handlers"
           ]

_MUMU_EXCEPTIONS = []


class _MumuExceptionMeta(type):
    def __new__(cls, name, bases, namespace):
        exc_cls = super().__new__(cls, name, bases, namespace)
        _MUMU_EXCEPTIONS.append(exc_cls)
        return exc_cls


class MumuException(Exception, metaclass=_MumuExceptionMeta):
    """Base Exception"""

    class Config:
        status_code: int = status.HTTP_400_BAD_REQUEST
        error_detail: str = "Something goes wrong"


class InsufficientAccessPermissionError(MumuException):
    """ 读取数据库的时候, 权限不足
    """

    class Config:
        status_code: int = status.HTTP_401_UNAUTHORIZED
        error_detail: str = "Permission denied"


class TagNotFoundError(MumuException):
    """在数据库找不到对应Tag"""

    class Config:
        status_code: int = status.HTTP_404_NOT_FOUND
        error_detail: str = "Tag not found"


class ItemNotFoundError(MumuException):
    """在数据库找不到对应的Item"""

    class Config:
        status_code: int = status.HTTP_404_NOT_FOUND
        error_detail: str = "Item not found"


def generate_exception_handler(exc_class: type):
    if not issubclass(exc_class, MumuException):
        raise TypeError("exc_class must be a MumuException")

    config = exc_class.Config

    def handler(request, exc):
        return JSONResponse(
            status_code=config.status_code,
            content={"error_message": config.error_detail,
                     "detail": str(exc)}
        )

    return handler


def register_exception_handlers(app: FastAPI):
    for cls in _MUMU_EXCEPTIONS:
        app.add_exception_handler(cls, generate_exception_handler(cls))
