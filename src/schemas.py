from typing import Union, TypeVar, Generic
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class LoanApplicationStatus(Enum):
    DRAFT = 1
    WITHDRAWN = 2
    COLLECTING_STAKE = 3
    FULLY_FUNDED = 4
    IN_PROGRESS = 5
    DEFAULT = 6
    COMPLETE = 7

class WalletType(Enum):
    WITHDRAW_ONLY = 1
    DEPOSIT_ONLY = 2
    WITHDRAW_OR_DEPOSIT = 3
    INTERNAL_ONLY = 4

class Wallet(object):
    def __init__(self, doc_id, wallet_type, address, key):
        self.doc_id = doc_id
        self.wallet_type: WalletType = wallet_type
        self.address: str = address
        self.key: str = key

class User(object):
    def __init__(self, uid):
        self.uid = uid

class LoanApplication(object):
    def __init__(
            self,
            doc_id,
            principal_in_xno,
            loan_start_date,
            monthly_payment,
            monthly_interest_rate,
            number_of_payment_periods,
            status,
            payment_wallet,
            principal_wallet,
            borrower):
        self.doc_id: str = doc_id
        self.principal_in_xno: float = principal_in_xno
        self.loan_start_date: datetime = loan_start_date
        self.monthly_payment: float = monthly_payment
        self.monthly_interest_rate: float = monthly_interest_rate
        self.number_of_payment_periods: int = number_of_payment_periods
        self.status: LoanApplicationStatus = status
        self.payment_wallet: Wallet = payment_wallet
        self.principal_wallet: Wallet = principal_wallet
        self.borrower: User = borrower

class Stake(object):
    def __init__(
            self,
            doc_id,
            owner,
            stake_start_date,
            stake_from_wallet,
            yield_wallet,
            monthly_interest_rate,
            monthly_payment,
            number_of_payment_periods):
        self.doc_id: str = doc_id
        self.owner: User = owner
        self.stake_start_date: datetime = stake_start_date
        self.stake_from_wallet: Wallet = stake_from_wallet
        self.yield_wallet: Wallet = yield_wallet
        self.monthly_interest_rate: float = monthly_interest_rate
        self.monthly_payment: float = monthly_payment
        self.number_of_payment_periods: float = number_of_payment_periods


class StakeTransfer(object):
    def __init__(self):
        pass

class LoanPaymentEvent(object):
    def __init__(self):
        pass
