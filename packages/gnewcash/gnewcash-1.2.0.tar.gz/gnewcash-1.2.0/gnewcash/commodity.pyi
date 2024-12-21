from _typeshed import Incomplete
from gnewcash.guid_object import GuidObject as GuidObject

class Commodity(GuidObject):
    commodity_id: Incomplete
    space: Incomplete
    get_quotes: Incomplete
    quote_source: Incomplete
    quote_tz: Incomplete
    name: Incomplete
    xcode: Incomplete
    fraction: Incomplete
    def __init__(self, commodity_id: str, space: str, guid: str | None = None, get_quotes: bool = False, quote_source: str | None = None, quote_tz: bool = False, name: str | None = None, xcode: str | None = None, fraction: str | None = None) -> None: ...
