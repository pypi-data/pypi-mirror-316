from _typeshed import Incomplete
from datetime import datetime
from decimal import Decimal
from gnewcash.account import Account as Account
from gnewcash.commodity import Commodity as Commodity
from gnewcash.guid_object import GuidObject as GuidObject
from gnewcash.slot import Slot as Slot, SlottableObject as SlottableObject
from gnewcash.transaction import ScheduledTransaction as ScheduledTransaction, SimpleTransaction as SimpleTransaction, SortingMethod as SortingMethod, Split as Split, Transaction as Transaction, TransactionManager as TransactionManager
from typing import Any, Generator

class GnuCashFile:
    books: Incomplete
    file_name: Incomplete
    def __init__(self, books: list['Book'] | None = None) -> None: ...
    @classmethod
    def read_file(cls, source_file: str, file_format: Any, sort_transactions: bool = True, sort_method: SortingMethod | None = None) -> GnuCashFile: ...
    def build_file(self, target_file: str, file_format: Any, prettify_xml: bool = False) -> None: ...
    def simplify_transactions(self) -> None: ...
    def strip_transaction_timezones(self) -> None: ...

class Book(GuidObject, SlottableObject):
    root_account: Incomplete
    transactions: Incomplete
    commodities: Incomplete
    template_root_account: Incomplete
    template_transactions: Incomplete
    scheduled_transactions: Incomplete
    budgets: Incomplete
    def __init__(self, root_account: Account | None = None, transactions: TransactionManager | None = None, commodities: list[Commodity] | None = None, slots: list[Slot] | None = None, template_root_account: Account | None = None, template_transactions: list[Transaction] | None = None, scheduled_transactions: list[ScheduledTransaction] | None = None, budgets: list['Budget'] | None = None, guid: str | None = None, sort_method: SortingMethod | None = None) -> None: ...
    def get_account(self, *paths_to_account: str, **kwargs: Any) -> Account | None: ...
    def get_account_balance(self, account: Account) -> Decimal: ...
    def get_all_accounts(self) -> Generator[Account | None, None, None]: ...

class Budget(GuidObject, SlottableObject):
    name: Incomplete
    description: Incomplete
    period_count: Incomplete
    recurrence_multiplier: Incomplete
    recurrence_period_type: Incomplete
    recurrence_start: Incomplete
    def __init__(self, guid: str | None = None, slots: list[Slot] | None = None, name: str | None = None, description: str | None = None, period_count: int | None = None, recurrence_multiplier: int | None = None, recurrence_period_type: str | None = None, recurrence_start: datetime | None = None) -> None: ...
