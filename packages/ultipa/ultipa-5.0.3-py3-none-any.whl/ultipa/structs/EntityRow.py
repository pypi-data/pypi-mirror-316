# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:21
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : EntityRow.py
from typing import Dict


class EntityRow:
	'''
	    Data class for data rows (nodes or edges) to be inserted.
	'''
	_index = None
	def __init__(self, values: Dict, schema: str = None, _id: str = None, _from: str = None, _to: str = None,
				 _uuid: int = None, _from_uuid: int = None, _to_uuid: int = None, **kwargs):
		self._uuid = _uuid
		self._id = _id
		self._from_uuid = _from_uuid
		self._to_uuid = _to_uuid
		self._from = _from
		self._to = _to
		if schema is None:
			if kwargs.get("schema_name") is not None:
				self.schema = kwargs.get("schema_name")
			else:
				self.schema = None
		else:
			self.schema = schema
		self.values = values

	def _getIndex(self):
		return self._index