from firebase_admin import firestore, auth, credentials, initialize_app
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Tuple, Any
from enum import Enum
from dotenv import load_dotenv
from dataclasses import dataclass, asdict, fields
from dacite import from_dict

from pathlib import Path
import os
import schemas
import datetime

# firebase / firestore setup
os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
load_dotenv(Path(os.environ['SECRETS_PATH']+"/.env.nanobank"))
initialize_app(credential=credentials.Certificate(os.environ['FIREBASE_CREDENTIALS_PATH']))
db = firestore.client()

# database
state_table = db.collection(u'state')
wallet_table = db.collection(u'wallet')
user_table = db.collection(u'user')
loan_table = db.collection(u'loan')
stake_table = db.collection(u'stake')
loan_payment_table = db.collection(u'loan_payment_event')

""" initial states """

def active_wallet_state() -> Tuple[Timestamp, Any]:
    _, ret = insert_state(schemas.State(
        state=schemas.WalletState.VALID_ACTIVE_WALLET,
        next=None,
        previous=None,
        timestamp=datetime.date.today()
    ))
    return ret

def initial_wallet_state() -> Tuple[Timestamp, Any]:
    _, ret = insert_state(schemas.State(
        state=schemas.WalletState.FROZEN_MISSING_USER_VERIFICATION,
        next=None,
        previous=None,
        timestamp=datetime.date.today()
    ))
    return ret

def initial_user_state() -> Tuple[Timestamp, Any]:
    _, ret = insert_state(schemas.State(
        state=schemas.UserState.CREATED,
        next=None,
        previous=None,
        timestamp=datetime.date.today()
    ))
    return ret

def initial_loan_state() -> Tuple[Timestamp, Any]:
    _, ret = insert_state(schemas.State(
        state=schemas.LoanApplicationState.DRAFT,
        next=None,
        previous=None,
        timestamp=datetime.date.today()
    ))
    return ret

def initial_loan_payment_state() -> Tuple[Timestamp, Any]:
    _, ret = insert_state(schemas.State(
        state=schemas.LoanPaymentState.SCHEDULED,
        next=None,
        previous=None,
        timestamp=datetime.date.today()
    ))
    return ret

""" end initial states """

def insert_internal_wallet(wallet: schemas.Wallet) -> Tuple[Timestamp, Any]:
    assert wallet.wallet_type == schemas.WalletType.INTERNAL_ONLY.value
    return wallet_table.add(asdict(wallet))

def insert_new_wallet_for_user(wallet: schemas.Wallet, user: schemas.User):
    _, wallet_ref = wallet_table.add(asdict(wallet))
    user.update({u'wallets': firestore.ArrayUnion([wallet_ref])})
    return _, wallet_ref

def insert_user(data: schemas.User) -> Tuple[Timestamp, Any]:
    return user_table.add(asdict(data))

def insert_loan(data: schemas.Loan) -> Tuple[Timestamp, Any]:
    return loan_table.add(asdict(data))

def insert_state(data: schemas.State) -> Tuple[Timestamp, Any]:
    return state_table.add(asdict(data))

def status_update(data: object, new_state: Enum):
    old_status = data.get().to_dict().get('status')
    _, new_status_ref = state_table.add(asdict(schemas.State(
        state = new_state,
        next = None,
        previous = old_status,
        timestamp = datetime.date.today()
    )))
    old_status.update({u'next': new_status_ref})
    data.update({u'status': new_status_ref})

# def append_state(old_state: schemas.State, new_state: schemas.State, parent: object):
#     # user.update(u'status.next': )
#     pass

# def update_user_state(status_obj: schemas.State, old_state: schemas.State, new_state: schemas.State):
#     pass

# def insert_stake(data: schemas.Stake) -> Tuple[Timestamp, Any]:
#     return stake_table.add(asdict(data))

# def insert_loan_payment(data: schemas.LoanPayment) -> Tuple[Timestamp, Any]:
#     return loan_payment_table.add(asdict(data))



# def insert_user_status(data: schemas.userStatus) -> Tuple[Timestamp, Any]:
#     pass

# def insert_wallet_status(data: schemas.WalletStatus) -> Tuple[Timestamp, Any]:
#     pass

# def insert_loan_application_status(data: schemas.LoanApplicationStatus) -> Tuple[Timestamp, Any]:
#     pass

# def insert_loan_payment_status(data: schemas.LoanPaymentStatus) -> Tuple[Timestamp, Any]:
#     pass