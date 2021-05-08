from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class ProxyErrorResponse(BaseModel):
    id: str
    error_code: str
    message: str

    def __init__(self, id: str, error_code: str, message: str) -> None:
        super().__init__(id=id, error_code=error_code, message=message)
