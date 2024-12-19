# -*- coding: utf-8 -*-
# @Time    : 2023/8/1 10:47
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Graph.py
from typing import List

from ultipa.structs.BaseModel import BaseModel

class GraphSet(BaseModel):


    def __init__(self, name: str,shards: List[str] = None, partitionBy: str = None, id: int = None, totalNodes: int = None,
                 totalEdges: int = None, description: str = None,slotNum :str = '', status: str = None):
        self.id = id
        self.name = name
        self.totalNodes = totalNodes
        self.totalEdges = totalEdges
        self.description = description
        self.status = status
        self.shards = shards
        self.slotNum = slotNum
        self.partitionBy = partitionBy



