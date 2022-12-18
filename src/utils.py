from firebase_admin import firestore, auth, credentials, initialize_app, DocumentReference
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Tuple
from dotenv import load_dotenv
from pathlib import Path
import os
import schemas

# firebase auth credentials
load_dotenv(Path(os.environ['SECRETS_PATH']+"/.env.nanobank"))
initialize_app(credential=credentials.Certificate(os.environ['FIREBASE_CREDENTIALS_PATH']))

# database
db = firestore.client()
wallet_status_table = db.collection(u'wallet_status')
loan_application_status_table = db.collection(u'loan_application_status')
loan_payment_status_table = db.collection(u'loan_payment_status')
wallet_table = db.collection(u'wallet')
user_table = db.collection(u'user')
loan_table = db.collection(u'loan')
stake_table = db.collection(u'stake')
loan_payment_table = db.collection(u'loan_payment_event')

def insert_wallet_status(data: schemas.WalletStatus) -> Tuple[Timestamp, DocumentReference]:
    return wallet_status_table.add(data.to_dict())

def insert_loan_application_status(data: schemas.LoanApplicationStatus) -> Tuple[Timestamp, DocumentReference]:
    return loan_application_status_table.add(data.to_dict())

def insert_loan_payment_status(data: schemas.LoanPaymentStatus) -> Tuple[Timestamp, DocumentReference]:
    return loan_payment_status_table.add(data.to_dict())

def insert_wallet(data: schemas.Wallet) -> Tuple[Timestamp, DocumentReference]:
    return wallet_table.add(data.to_dict())

def insert_user(data: schemas.User) -> Tuple[Timestamp, DocumentReference]:
    return user_table.add(data.to_dict())

def insert_loan(data: schemas.Loan) -> Tuple[Timestamp, DocumentReference]:
    return loan_table.add(data.to_dict())

def insert_stake(data: schemas.Stake) -> Tuple[Timestamp, DocumentReference]:
    return stake_table.add(data.to_dict())

def insert_loan_payment(data: schemas.LoanPayment) -> Tuple[Timestamp, DocumentReference]:
    return loan_payment_table.add(data.to_dict())
