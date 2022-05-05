from ..api_data.qry_component import QryComponent
from ..api_data.qry_module_info import QryModuleInfo
from ..data_class.component import Component
from ..data_class.module_info import ModuleInfo
from ..api_data.db_connect import DbConnect
from typing import List

def search_component(search: str, limit:int = 0) -> List[Component]:
    db_con = DbConnect()
    qry = QryComponent(connect_str=db_con.connection_str)
    return qry.get_components(search_str=search, limit=limit)


def search_module_info(search: str, limit: int = 0) -> List[ModuleInfo]:
    db_con = DbConnect()
    qry = QryModuleInfo(connect_str=db_con.connection_str)
    return qry.get_mod_infos(search_str=search, limit=limit)
