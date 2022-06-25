# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: meta.py 
@time: 2022/06/25
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""
from version import __version__

__all__ = ["MUMU_GLOBAL_META"]

MUMU_GLOBAL_META = {
    "title": "Mumu Memo Server",
    "version": __version__,
    "description": "Mumu Memo 备忘录API文档",
    "contact": {
        "name": "Jianzhang Chen",
        "url": "https://jeza-chen.com",
        "email": "jeza@vip.qq.com"
    },
    "license_info": {
        "name": "GPL-3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html"
    },
}
