# -*- coding: utf-8 -*-
# @Time    : 2023/8/4 16:36
# @Author  : Ultipa
# @Email   : support@ultipa.com
# @File    : Algo.py
from ultipa.structs.BaseModel import BaseModel


class Algo(BaseModel):
	'''
	    Data class for algorithm.
	'''
	name: str
	description: str
	version: str
	result_opt: str
	parameters: dict
	# write_to_stats_parameters: dict
	write_to_db_parameters: dict
	write_to_file_parameters: dict
	# write_to_client_normal_parameters:dict
	# write_to_client_stream_parameters:dict

	def __init__(self,name:str,description:str,version:str,result_opt:str,parameters:dict,
			  write_to_stats_parameters:dict=None,write_to_db_parameters:dict=None,
			  write_to_file_parameters:dict=None
			#   write_to_client_normal_parameters:dict=None,
			#   write_to_client_stream_parameters:dict=None
			  ):
		self.name = name
		self.description = description
		self.version = version
		self.result_opt = result_opt
		self.parameters = parameters
		# self.write_to_stats_parameters = write_to_stats_parameters
		self.write_to_db_parameters=write_to_db_parameters
		self.write_to_file_parameters=write_to_file_parameters
		# self.write_to_client_normal_parameters=write_to_client_normal_parameters
		# self.write_to_client_stream_parameters=write_to_client_stream_parameters


class AlgoResultOpt(BaseModel):
	can_realtime: bool
	can_visualization: bool
	can_write_back: bool

class ALGO_RESULT:
	ALGO_RESULT_UNSET = -1
	WRITE_TO_FILE = 1
	WRITE_TO_DB = 2
	WRITE_TO_CLIENT = 4
	WRITE_TO_VISUALIZATION = 8

class HDCAlgo(BaseModel):

	def __init__(self,name:str,version:float,type:str,subsType:str,writeSupportType:str,canRollback:str,description:str,configContext:str):
		self.name = name
		self.version = version
		self.type = type
		self.subsType = subsType
		self.writeSupporType = writeSupportType
		self.canRollback = canRollback
		self.description = description
		self.configContext = configContext