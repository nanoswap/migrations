from __future__ import annotations
from typing import Union, List
from datetime import datetime, date
from enum import Enum
from dataclasses import dataclass, asdict, fields, field
from dacite import from_dict
from random import random

""" Enums """

class WalletType(Enum):
    WITHDRAW_ONLY = 1  # yield wallet
    DEPOSIT_ONLY = 2  # bill pay wallet
    WITHDRAW_OR_DEPOSIT = 3  # personal wallet
    INTERNAL_ONLY = 4  # internal wallet

class UserState(Enum):
    CREATED = 1
    VALIDATION_IN_PROGRESS = 2
    VALIDATION_FAILED = 3
    ACTIVE = 4
    FROZEN = 5

class WalletState(Enum):
    FROZEN_MISSING_USER_VERIFICATION = 1
    FROZEN_FRAUD_SUSPECTED = 2
    FROZEN_STAKED_FOR_LOAN = 3
    VALID_ACTIVE_WALLET = 4

class LoanApplicationState(Enum):
    DRAFT = 1
    WITHDRAWN = 2
    COLLECTING_STAKE = 3
    FULLY_FUNDED = 4
    IN_PROGRESS = 5
    DEFAULT = 6
    COMPLETE = 7

class LoanPaymentState(Enum):
    SCHEDULED = 1
    UPCOMING = 2
    COMPLETED_ON_TIME = 3
    LATE = 4
    COMPLETED_LATE = 5
    MISSED = 6

""" Object Status Class (for tracking entity workflows) """

@dataclass
class State:
    state: int
    enum_type: type
    next: Union[State, None]
    previous: Union[State, None]
    timestamp: datetime
    doc_id: str = random()

    def __post_init__(self):
        self.state = self.state.value
        self.enum_type = str(self.enum_type)
        self.timestamp = int(self.timestamp.strftime('%s'))
    
    def __repr__(self):
        return {
            "state": self.enum_type(self.state),
            "next": self.next,
            "previous": self.previous,
            "timestamp": self.timestamp
        }

""" Entities """

@dataclass
class User:
    uid: str
    status: State
    wallets: List[Wallet] = field(default_factory=list)

@dataclass
class Wallet:
    wallet_type: WalletType
    address: str
    status: State
    key: Union[str, None] = None
    doc_id: float = random()

    def __post_init__(self):
        self.wallet_type = self.wallet_type.value

@dataclass
class Loan:
    principal_in_xno: float
    start_date: datetime
    monthly_payment: float
    monthly_interest_rate: float
    number_of_payment_periods: int
    payment_wallet: Wallet
    principal_wallet: Wallet
    borrower: User
    status: State
    doc_id: float = random()

    def __post_init__(self):
        self.start_date = int(self.start_date.strftime('%s'))
    
@dataclass
class Stake:
    owner: User
    start_date: datetime
    from_wallet: Wallet
    yield_wallet: Wallet
    monthly_interest_rate: float
    monthly_payment: float
    number_of_payment_periods: float
    doc_id: float = random()

    def __post_init__(self):
        self.start_date = int(self.start_date.strftime('%s'))

@dataclass
class LoanPayment:
    loan: Loan
    due_date: datetime
    amount_due_in_xno: float
    status: State
    doc_id: float = random()

    def __post_init__(self):
        self.due_date = int(self.due_date.strftime('%s'))
