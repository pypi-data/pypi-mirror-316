import time

import json
from typing import Tuple, List

from ultipa.configuration.RequestConfig import RequestConfig
from ultipa.operate.base_extra import BaseExtra
from ultipa.structs import Graph
from ultipa.types import ULTIPA, ULTIPA_RESPONSE
from ultipa.types.types import Status, Code
from ultipa.utils import UQLMAKER, CommandList
from ultipa.utils.ResposeFormat import ResponseKeyFormat
from ultipa.utils.convert import convertToGraph
from ultipa.structs.GraphSet import GraphSet
REPLACE_KEYS = {
	"graph": "name",
}


class GraphExtra(BaseExtra):
	'''
	Processing class that defines settings for graphset related operations.
	'''

	def uqlCreateSubgraph(self, uql: str, subGraphName: str, requestConfig: RequestConfig = RequestConfig()):
		ret = self.uql(uql, requestConfig)
		graphRet = self.getGraph(subGraphName)
		if graphRet:
			self.createGraph(GraphSet(name=subGraphName))
			time.sleep(3)

	def showGraph(self, requestConfig: RequestConfig = RequestConfig()) ->List[GraphSet]:
		'''
		Acquire graphset list.

		Args:
			requestConfig: An object of RequestConfig class

		Returns:
			List[GraphSet]
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraphMore, commonParams=requestConfig)
		uqlMaker.setCommandParams("")
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		if res.status.code ==0 :
			res.data = convertToGraph(res)
			return res.data
		return ULTIPA_RESPONSE.UltipaResponse(status=res.status)
		# uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		# uqlMaker.setCommandParams("")
		# res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		# res.data = convertToGraph(res)
		# return res.data

	def getGraph(self, graphName: str,
				 requestConfig: RequestConfig = RequestConfig()) -> GraphSet:
		'''
		Acquire a designated graphset.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			GraphSet
		'''

		uqlMaker = UQLMAKER(command=CommandList.showGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)
		uqlMaker.addParam(key='more',value=graphName)
		res = self.UqlListSimple(uqlMaker=uqlMaker, responseKeyFormat=ResponseKeyFormat(keyReplace=REPLACE_KEYS))
		if res.status.code == ULTIPA.Code.SUCCESS:
			res.data = convertToGraph(res)
		else:
			res.data = None
		return res.data

	def createGraph(self, graph: GraphSet,
					config: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Create a graphset.

		Args:
			grpah: An object of Graph class

			config: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''
		uqlMaker = UQLMAKER(command=CommandList.createGraph, commonParams=config)
		if graph.shards and  graph.partitionBy:
			shardslist=[int(shard) for shard in graph.shards]
			if graph.description:
				uqlMaker.setCommandParams([graph.name, graph.description])

			else:
				uqlMaker.setCommandParams(graph.name)
			uqlMaker.addParam(key='shards', value=shardslist)
			uqlMaker.addParam(key='partitionByHash', value=f"'{graph.partitionBy}',_id")
			res = self.uqlSingle(uqlMaker)
			return res
		else:
			message = 'partitionBy and shards is empty' if not graph.shards and  not graph.partitionBy else 'shards is empty' if not graph.shards else 'partitionBy is empty'

			return ULTIPA_RESPONSE.UltipaResponse(status=Status(code = Code.FAILED,message=message))


	def dropGraph(self, graphName: str,
				  requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		Drop a graphset.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			UltipaResponse
		'''

		uqlMaker = UQLMAKER(command=CommandList.dropGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(graphName)
		res = self.uqlSingle(uqlMaker)
		return res

	def alterGraph(self, oldGraph: GraphSet, newGraph: GraphSet,
			   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		'''
		        Alter a graphset

		        Args:
		            oldGraphName: The orignal name of graphset

		            newGraphName: The new name of graphset

		            newDescription: The new description of graphset

		            requestConfig: An object of RequestConfig class

		        Returns:
		            UltipaResponse
		        '''

		requestConfig.graphName = oldGraph.name
		uqlMaker = UQLMAKER(command=CommandList.alterGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(oldGraph.name)
		data = {"name": newGraph.name}
		if newGraph.description is not None:
			data.update({'description': newGraph.description})
		uqlMaker.addParam("set", data)
		res = self.uqlSingle(uqlMaker)
		return res

	def hasGraph(self, graphName: str, requestConfig: RequestConfig = RequestConfig()) -> bool:
		'''
				Check if graph exists or not.

				Args:
					graphName: The name of graphset

					requestConfig: An object of RequestConfig class

				Returns:
					bool
				'''

		graphsdata = self.showGraph(requestConfig)
		for graphs in graphsdata:
			if (graphs.name == graphName):
				return True

		return False

	def createGraphIfNotExist(self, graph: GraphSet,
							  config: RequestConfig = RequestConfig()) -> Tuple[
		bool, ULTIPA_RESPONSE.UltipaResponse]:
		'''
		Checks if graph exists or not, if graph does not exist then creates new.

		Args:
			graphName: The name of graphset

			requestConfig: An object of RequestConfig class

		Returns:
			bool
			UltipaResponse
		'''

		if (self.hasGraph(graph.name, config)) == True:
			return [True, None]

		else:
			res = self.createGraph(graph,config = config)
			return [False, res]

	def rebalanceGraph(self,name: str,shards:List[str],
					   requestConfig: RequestConfig = RequestConfig()) -> ULTIPA_RESPONSE.UltipaResponse:
		"""
		graph migrate
		name: The name of graph
		shards: The shards of new shards
		"""
		shardslist = [int(shard) for shard in shards]
		uqlMaker = UQLMAKER(command=CommandList.rebalanceGraph, commonParams=requestConfig)
		uqlMaker.setCommandParams(name)
		uqlMaker.addParam(key='shards', value=shardslist)
		res = self.uqlSingle(uqlMaker)
		return res