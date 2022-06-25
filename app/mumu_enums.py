# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: mumu_enums.py 
@time: 2022/06/25
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""

import enum

__all__ = ["ItemState"]


class ItemState(str, enum.Enum):
    """备忘事项的状态"""
    TODO = "todo"
    ONGOING = "ongoing"
    DONE = "done"
