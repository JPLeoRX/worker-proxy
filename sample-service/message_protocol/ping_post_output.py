from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class PingPostOutput(BaseModel):
    id: str
    success: bool
    text: str

    def __init__(self, id: str, success: bool, text: str) -> None:
        super().__init__(id=id, success=success, text=text)
