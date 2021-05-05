import uuid
from injectable import injectable


@injectable
class UtilsId:
    def generate_uuid(self) -> str:
        return str(uuid.uuid4())
