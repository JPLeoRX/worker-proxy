from typing import Any, Dict
from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class ProxyResponse(BaseModel):
    content: Any
    status_code: int
    headers: Dict[str, Any]

    def __init__(self, content: Any, status_code: int, headers: Dict[str, Any]) -> None:
        super().__init__(content=content, status_code=status_code, headers=headers)
