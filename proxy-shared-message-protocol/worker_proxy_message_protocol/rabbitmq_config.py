from pydantic import BaseModel
from simplestr import gen_str_repr


@gen_str_repr
class RabbitmqConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str

    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        super().__init__(host=host, port=port, username=username, password=password)
