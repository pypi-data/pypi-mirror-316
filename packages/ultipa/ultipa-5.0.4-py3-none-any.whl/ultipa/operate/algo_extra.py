import hashlib
import os
from typing import List

from ultipa.structs import Algo

from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.proto import ultipa_pb2
from ultipa.structs.Algo import ALGO_RESULT, HDCAlgo
from ultipa.types import ULTIPA_REQUEST, ULTIPA, ULTIPA_RESPONSE
from ultipa.types.types import Exta
from ultipa.utils import UQLMAKER, CommandList, errors
from ultipa.utils.fileSize import read_in_chunks
from ultipa.utils.format import FormatType
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertToAlgo, convertToExta


class AlgoExtra(BaseExtra):
	'''
		Processing class that defines settings for algorithm related operations.

	'''
	JSONSTRING_KEYS = ["param"]


	def showExta(self,config: RequestConfig = RequestConfig())-> List[Exta]:
		'''
		Query for algorithm list.

		Args:
			config: An object of the RequestConfig class

		Returns:
			ResponseListAlgo

		'''
		uqlMaker = UQLMAKER(command=CommandList.showExta, commonParams=config)
		res = self.UqlListSimple(uqlMaker)
		if res.status.code == ULTIPA.Code.SUCCESS:
			res.data = convertToExta(res)
			return res.data
		else :
			return res

	def __make_message(self, fileName, md5, chunk, hdcName):
		return ultipa_pb2.InstallAlgoRequest(
			file_name=fileName, md5=md5, chunk=chunk, with_server=ultipa_pb2.WithServer(hdc_server_name=hdcName)
		)

	def __generate_messages(self, request: ULTIPA_REQUEST.InstallAlgo):
		messages = []
		file_object = open(request.soPath, 'rb')
		hdcName = request.hdcName
		somd5 = hashlib.md5(file_object.read()).hexdigest()
		file_object.close()

		for chunk in read_in_chunks(request.soPath):
			fileName = os.path.basename(request.soPath)
			messages.append(self.__make_message(fileName, somd5, chunk, hdcName))

		file_object = open(request.configPath, 'rb')
		configmd5 = hashlib.md5(file_object.read()).hexdigest()
		file_object.close()
		for chunk in read_in_chunks(request.configPath):
			fileName = os.path.basename(request.configPath)
			messages.append(self.__make_message(fileName, configmd5, chunk, hdcName))
		for msg in messages:
			yield msg

	def installAlgo(self, soFilePath: str, infoFilePath: str,
					config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Install an Ultipa standard algorithm.

		Args:
			soFilePath: The directory of the algorithm package (.so)

			infoFilePath: The directory of the algorithm configuration (.yml)

			config: An object of the RequestConfig class

		Returns:
			Response

		'''
		request = ULTIPA_REQUEST.InstallAlgo(infoFilePath, soFilePath)
		clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster,
										isGlobal=True)
		response = ULTIPA_RESPONSE.UltipaResponse()
		try:
			if os.path.exists(request.soPath) and os.path.exists(request.configPath):
				installRet = clientInfo.Controlsclient.InstallAlgo(self.__generate_messages(request),
																   metadata=clientInfo.metadata)
				status = FormatType.status(installRet.status)
				response.status = status
		except Exception as e:
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
			except:
				message = str(e)

			response.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)

		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "InstallAlgo",
											config.useHost if config.useHost else self.host,
											config.retry,
											False)
		return response

	def uninstallAlgo(self, algoName: str,
					  config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Uninstall an Ultipa standard algorithm.

		Args:
			algoName: The name of algorithm

			config: An object of the RequestConfig class

		Returns:
			Response

		'''
		clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster,
										isGlobal=True)
		arequest = ultipa_pb2.UninstallAlgoRequest(algo_name=algoName)
		installRet = clientInfo.Controlsclient.UninstallAlgo(arequest, metadata=clientInfo.metadata)
		status = FormatType.status(installRet.status)
		response = ULTIPA_RESPONSE.UltipaResponse(status=status)
		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "UnInstallAlgo",
											config.useHost if config.useHost else self.host,
											config.retry,
											False)
		return response


	def installHDCAlgo(self, soFile: str, ymlFile: str,hdcName:str,
					config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Install an Ultipa standard algorithm.

		Args:
			soFile: The directory of the algorithm package (.so)

			ymlFile: The directory of the algorithm configuration (.yml)

			hdcName: The name of the hdc

			config: An object of the RequestConfig class

		Returns:
			UltipaResponse

		'''
		request = ULTIPA_REQUEST.InstallAlgo(ymlFile, soFile,hdcName)
		clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster,
										isGlobal=True)
		response = ULTIPA_RESPONSE.Response()
		try:
			if os.path.exists(request.soPath) and os.path.exists(request.configPath):
				installRet = clientInfo.Controlsclient.InstallAlgo(self.__generate_messages(request),
																   metadata=clientInfo.metadata)
				status = FormatType.status(installRet.status)
				response.status = status
		except Exception as e:
			try:
				message = str(e._state.code) + ' : ' + str(e._state.details)
			except:
				message = str(e)

			response.status = ULTIPA.Status(code=ULTIPA.Code.UNKNOW_ERROR, message=message)

		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "InstallAlgo",
											config.useHost if config.useHost else self.host,
											config.retry,
											False)
		return response

	def uninstallHDCAlgo(self, algoName: str,hdcName:str,
					  config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Uninstall an Ultipa standard algorithm.

		Args:
			algoName: The name of algorithm

			hdcName: The name of hdc

			config: An object of the RequestConfig class

		Returns:
			Response

		'''
		clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster,
										isGlobal=True)
		arequest = ultipa_pb2.UninstallAlgoRequest(algo_name=algoName, with_server=ultipa_pb2.WithServer(hdc_server_name=hdcName))
		installRet = clientInfo.Controlsclient.UninstallAlgo(arequest, metadata=clientInfo.metadata)
		status = FormatType.status(installRet.status)
		response = ULTIPA_RESPONSE.UltipaResponse(status=status)
		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "UnInstallAlgo",
											config.useHost if config.useHost else self.host,
											config.retry,
											False)
		return response

	def rollbackHDCAlgo(self,algoName :str,hdcName:str
						,config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		"""
		Args:
			algoName: The name of algorithm

			hdcName: The name of hdc

			config: An object of the RequestConfig class

		Returns:
			Response
		"""
		clientInfo = self.getClientInfo(graphSetName=config.graphName, useMaster=config.useMaster,
										isGlobal=True)
		arequest = ultipa_pb2.RollbackAlgoRequest(algo_name=algoName,
												   with_server=ultipa_pb2.WithServer(hdc_server_name=hdcName))
		rollbackRet = clientInfo.Controlsclient.RollbackAlgo(arequest, metadata=clientInfo.metadata)
		status = FormatType.status(rollbackRet.status)
		response = ULTIPA_RESPONSE.UltipaResponse(status=status)
		if self.defaultConfig.responseWithRequestInfo:
			response.req = ULTIPA.ReturnReq(self.graphSetName, "RollbackAlgo",
											config.useHost if config.useHost else self.host,
											config.retry,
											False)
		return response

	def showHDCAlgo(self,hdcName:str
						,config: RequestConfig = RequestConfig()) -> List[HDCAlgo]:
		"""
		Args:
			hdcName: The name of hdc

			config: An object of the RequestConfig class

		Returns:
			Response
		"""
		command=CommandList.showHDCAlgo
		commandp=f"'{hdcName}'"
		uqlMaker = UQLMAKER(command=command, commandP=commandp, commonParams=config)
		res=self.uqlSingle(uqlMaker)
		result = None
		if res.status.code == 0:
			if res.alias(f"_algoList_from_{hdcName}").data:
				result = res.alias(f"_algoList_from_{hdcName}").asHDCAlgos()



		return result
