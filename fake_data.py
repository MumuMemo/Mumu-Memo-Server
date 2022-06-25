# -*- coding:utf-8 _*-
""" 
@author: Jeza Chen
@license: GPL-3.0 License
@file: fake_data.py 
@time: 2022/06/19
@contact: jeza@vip.qq.com
@site:  
@software: PyCharm 
@description: 
"""

fake_tags: dict[str, dict] = {
    "0": {
        "tag_id": "0",
        "title": "学习",
        "parent_tag": "",
        "child_tags": ["1", "2"],
        "items": ["0", "2"]
    },
    "1": {
        "tag_id": "1",
        "title": "Python学习",
        "parent_tag": "0",
        "child_tags": [],
        "items": ["1", "2"]
    },
    "2": {
        "tag_id": "2",
        "title": "C#学习",
        "parent_tag": "0",
        "child_tags": [],
        "items": ["2"]
    }
}

fake_items: dict[str, dict] = {
    "0": {
        "item_id": "0",
        "title": "学习一门新的语言",
        "linked_tags": ["0"],
        "content": "学习学习\n学习学习",
        "remind_timestamp": 1655627407,
    },
    "1": {
        "item_id": "1",
        "title": "Python迭代器学习",
        "linked_tags": ["1"],
        "content": "学习学习\n学习学习",
        "remind_timestamp": 1655627807,
    },
    "2": {
        "item_id": "2",
        "title": "Python/C#混合编程学习",
        "linked_tags": ["1", "2"],
        "content": "学习学习\n学习学习",
        "remind_timestamp": 1655627807,
    }
}