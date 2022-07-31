"""
    Domain Modeling
"""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import NamedTuple, Optional, Set
from pydantic import BaseModel

@dataclass(frozen=True)
class Name:
    first_name: str
    last_name: str

class Money(NamedTuple):
    currency: str
    value: int

@dataclass(frozen=True)
class Person:
    name: Name
    date_of_birth: date

    @property
    def age(self) -> timedelta:
        return date.today() - self.date_of_birth

    @property
    def age_in_years(self) -> float:
        return round(self.age.days/365.25,2)

@dataclass(frozen=True)
class OrderLine:
    """Immutable class with no behavior"""
    orderid: str
    sku: str
    qty: int

class Batch:
    reference:str
    sku: str
    eta: Optional[date]
    _purchased_quantity: int
    _allocations: Set[OrderLine]

    def __init__(self, ref:str, sku:str, qty:int, eta:Optional[date]) -> None:
        """Constructor"""
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line:OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


    def allocate(self, line:OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line:OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Batch):
            return False
        return __o.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, __o: object) -> bool:
        if self.eta is None:
            return False
        if __o.eta is None:
            return True
        return self.eta > __o.eta