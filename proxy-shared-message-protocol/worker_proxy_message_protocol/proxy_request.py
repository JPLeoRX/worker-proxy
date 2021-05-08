from typing import Dict, Any, Tuple
from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class ProxyRequest(BaseModel):
    method: str
    url: str
    base_url: str
    headers: Dict[str, Any]
    query_params: Dict[str, Any]
    path_params: Dict[str, Any]
    cookies: Dict[str, Any]
    body: Any
    client: Tuple[str, str]

    def __init__(self, method: str, url: str, base_url: str, headers: Dict[str, Any], query_params: Dict[str, Any], path_params: Dict[str, Any], cookies: Dict[str, Any], body: Any, client: Tuple[str, str]) -> None:
        super().__init__(method=method, url=url, base_url=base_url, headers=headers, query_params=query_params, path_params=path_params, cookies=cookies, body=body, client=client)
