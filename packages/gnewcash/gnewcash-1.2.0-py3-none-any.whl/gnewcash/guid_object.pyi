from _typeshed import Incomplete

class GuidObject:
    used_guids: set[str]
    guid: Incomplete
    def __init__(self, guid: str | None = None) -> None: ...
    @classmethod
    def get_guid(cls) -> str: ...
