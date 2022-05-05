from ..api_data.qry_component import QryComponent
from ..data_class.component import Component
from ..api_data.db_connect import DbConnect
from typing import List

def search_component(search: str, limit:int = 0) -> List[Component]:
    db_con = DbConnect()
    qry = QryComponent(connect_str=db_con.connection_str)
    return qry.get_components(search_str=search, limit=limit)