from typing import List, Dict
from ultipa.printer.prettyPrint import PrettyPrint, PrettyTable
from ultipa.structs.GraphSet import GraphSet
from ultipa.structs.Property import Property
from ultipa.structs.Schema import Schema
from ultipa.structs.DBType import DBType
from ultipa.structs.User import User
from ultipa.structs.Policy import Policy
from ultipa.structs.Privilege import Privilege
from ultipa.structs.Index import Index
from ultipa.structs.Stats import Stats
from ultipa.structs.Top import Top
from ultipa.structs.Algo import Algo
from ultipa.types.types import BaseModel, Node, Edge, DataItem, Status, \
    UltipaStatistics, ReturnReq, BaseUqlReply, ResultType, ResultAlias, ExplainPlan
from ultipa.utils.convert import Any
from typing import Callable


class PropertyTable(BaseModel):
    name: str
    data: List[Property]

    def __init__(self, name, data):
        self.name = name
        self.data = data


class Response(BaseModel):
    def __init__(self, status: Status = None, data: BaseUqlReply = None,
                 req: ReturnReq = None, statistics: UltipaStatistics = None, aliases: List[ResultAlias] = None):
        self.status = status
        self.data = data
        self.statistics = statistics
        self.req = req
        self.aliases = aliases

    def Print(self):
        pretty = PrettyPrint()
        pretty.prettyStatus(self.status)
        if self.status.code != 0:
            return
        if self.statistics:
            pretty.prettyStatistics(self.statistics)

        if isinstance(self.data, list):
            dict_list = []
            for i in self.data:
                if isinstance(i, PropertyTable):
                    dict_list.append(i.toDict())
                else:
                    dict_list.append(i.__dict__)
            pretty.prettyDataList(dict_list)

        if isinstance(self.data, Any):
            dict_list = self.data.__dict__
            pretty.prettyData(dict_list)


class UltipaResponse(BaseModel):
    def __init__(self, status: Status = None, items: Dict = None,
                 req: ReturnReq = None, statistics: UltipaStatistics = None, aliases: List[ResultAlias] = None,
                 explainPlan: List[ExplainPlan] = None):
        self.status = status
        self.items = items
        self.aliases = aliases
        self.req = req
        self.statistics = statistics
        self.explainPlan = explainPlan

    def alias(self, alias: str) -> DataItem:
        if self.items == None:
            return DataItem(alias, None, ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET))
        if self.items.get(alias):
            return self.items.get(alias)
        return DataItem(alias, None, ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET))

    def aliasItem(self, alias: str) -> DataItem:
        if self.items == None:
            return DataItem(alias, None, ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET))
        if self.items.get(alias):
            return DataItem(alias, self.items[f'{alias}'].data, ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE))
        return DataItem(alias, None, ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET))

    def get(self, index: int) -> DataItem:
        if len(self.aliases) - 1 >= index:
            data = self.items.get(self.aliases[index].alias)
            if data:
                return data
            if self.aliases[index].result_type == ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET):
                return DataItem(None, None, ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET))
        return DataItem(None, None, ResultType.getTypeStr(ResultType.RESULT_TYPE_UNSET))

    def getExplainPlan(self):
        return self.explainPlan

    def Print(self):
        pretty = PrettyPrint()
        pretty.prettyStatus(self.status)
        if self.status.code != 0:
            return
        pretty.prettyStatistics(self.statistics)
        explains = []
        for key in self.items:
            dataItem = self.items.get(key)
            if dataItem.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_NODE):
                pretty.prettyNode(dataItem)

            elif dataItem.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_EDGE):
                pretty.prettyEdge(dataItem)

            elif dataItem.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_TABLE):
                pretty.prettyTable(dataItem)

            elif dataItem.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_PATH):
                pretty.prettyPath(dataItem)

            elif dataItem.type == ResultType.getTypeStr(ResultType.RESULT_TYPE_ATTR):
                pretty.prettyAttr(dataItem)

        if self.explainPlan:
            for explan in self.explainPlan:
                explains.append(explan)
            if explains:
                pretty.prettyTree(explains)


class UQLResponseStream:
    def __init__(self):
        self._listeners = {}
        self._default_handlers = {
            "start": self._default_start_handler,
            "end": self._default_end_handler
        }

    def on(self, event: str, handler: Callable):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(handler)

    def emit(self, event: str, *args, **kwargs):
        if event in self._listeners:
            for handler in self._listeners[event]:
                handler(*args, **kwargs)
        elif event in self._default_handlers:
            self._default_handlers[event](*args, **kwargs)

    def _default_start_handler(self, request_config):
        print("Stream started with request:", request_config)

    def _default_end_handler(self, request_config):
        print("Stream ended with request:", request_config)


class ResponseCommon(Response):
    data: None


# class User(BaseModel):
# 	username: str
# 	create: str
# 	last_login_time: str
# 	graphPrivileges: dict
# 	systemPrivileges: List[str]
# 	policies: List[str]


# class Index(BaseModel):
# 	name: str
# 	properties: str
# 	schema: str
# 	status: str
# 	size:str
# 	dbType:DBType


# class IndexTable:
# 	name: str
# 	data: List[Index]


class Stat(BaseModel):
    cpuUsage: str
    memUsage: str
    company: str
    cpuCores: str
    expiredDate: str
    serverType: str
    version: str


# class Privilege(BaseModel):
# 	graphPrivileges: List[str]
# 	systemPrivileges: List[str]


# class Policy(BaseModel):
# 	name: str
# 	policies: List[str]
# 	graphPrivileges: dict
# 	systemPrivileges: List[str]


# class Top(BaseModel):
# 	process_id: str
# 	process_uql: str
# 	duration: str


class Return_Type(BaseModel):
    is_realtime: bool
    is_visualization: bool
    is_wirte_back: bool


class Task_info(BaseModel):
    task_id: int = None
    server_id: int = None
    algo_name: str = None
    start_time: int = None
    writing_start_time: int = None
    end_time: int = None
    time_cost: int = None
    TASK_STATUS: int = None
    status_code: str = None
    engine_cost: int = None
    return_type: Return_Type = None


class Task(BaseModel):
    param: dict
    task_info: Task_info
    result: dict


class SearchKhop(BaseModel):
    values: dict
    nodes: List[Node]


class Path(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


class SearchPath(BaseModel):
    paths: List[Path]


class NodeSpread(SearchPath):
    pass


class AutoNet(SearchPath):
    pass


class AlgoResultOpt(BaseModel):
    can_realtime: bool
    can_visualization: bool
    can_write_back: bool


class Exta(BaseModel):
    author: str
    detail: str
    name: str
    version: str


# class Algo(BaseModel):
# 	param: dict
# 	name: str
# 	result_opt: AlgoResultOpt

class ResponseGraph(Response):
    data: GraphSet


class ResponseListGraph(Response):
    data: List[GraphSet]


class ResponeListExta(Response):
    data: List[Exta]

class ResponseSchema(Response):
    items: Schema


class ResponseListSchema(UltipaResponse):
    items: List[Schema]


class ResponseListIndex(UltipaResponse):
    data: List[Index]


# class ResponseListFulltextIndex(ResponseListIndex):
# 	pass


class ResponseSearchEdge(UltipaResponse):
    items: List[DataItem]


class ResponseSearchNode(UltipaResponse):
    items: List[DataItem]


class ResponseBulk:
    uuids: List[int]
    errorItem: Dict


class ResponseInsertNode(UltipaResponse):
    data: List[Node]


class ResponseInsertEdge(UltipaResponse):
    data: List[Edge]


class ResponseDeleteNode(UltipaResponse):
    data: List[Node]


class ResponseDeleteEdge(UltipaResponse):
    data: List[Edge]


class ResponseBatchAutoInsert(Response):
    data: Dict[str, ResponseBulk]


class InsertResponse(Response):
    data: ResponseBulk


class ResponseListPolicy(Response):
    data: List[Policy]


class ResponsePolicy(Response):
    data: Policy


class ResponsePrivilege(Response):
    data: List[Privilege]


class ResponseListProperty(UltipaResponse):
    items: List[Property]


class ResponseProperty(Response):
    data: List[Property]


class ResponseListTop(Response):
    data: List[Top]


class ResponseListTask(Response):
    data: List[Task]


class ResponseUser(Response):
    data: User


class ResponseListUser(Response):
    data: List[User]


class ResponseListAlgo(Response):
    data: List[Algo]


class Cluster:
    host: str
    status: bool
    cpuUsage: str
    memUsage: str
    isLeader: bool
    isFollowerReadable: bool
    isAlgoExecutable: bool
    isUnset: bool


class ClusterInfo(Response):
    data: List[Cluster]


class ResponseStat(Response):
    data: Stats


class ResponseExport(Response):
    data: List[Node]


