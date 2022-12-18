from firebase_admin import firestore, auth, credentials, initialize_app
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Tuple, Any
from dotenv import load_dotenv
from dataclasses import dataclass, asdict, fields
from dacite import from_dict

from pathlib import Path
import os
import schemas

# firebase / firestore setup

os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
load_dotenv(Path(os.environ['SECRETS_PATH']+"/.env.nanobank"))
initialize_app(credential=credentials.Certificate(os.environ['FIREBASE_CREDENTIALS_PATH']))
db = firestore.client()

# database
wallet_table = db.collection(u'wallet')
user_table = db.collection(u'user')
loan_table = db.collection(u'loan')
stake_table = db.collection(u'stake')
loan_payment_table = db.collection(u'loan_payment_event')



def insert_wallet(data: schemas.Wallet) -> Tuple[Timestamp, Any]:
    return wallet_table.add(asdict(data))

def insert_user(data: schemas.User) -> Tuple[Timestamp, Any]:
    return user_table.add(asdict(data))

def insert_loan(data: schemas.Loan) -> Tuple[Timestamp, Any]:
    return loan_table.add(asdict(data))

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