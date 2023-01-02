from firebase_admin import firestore, auth, credentials, initialize_app, exceptions
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Tuple, Any, List
from enum import Enum
from dotenv import load_dotenv
from dataclasses import dataclass, asdict, fields
from dacite import from_dict
from faker import Faker

Faker.seed(0)
fake = Faker()

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

active_wallet_state = lambda: initial_state(schemas.WalletState.VALID_ACTIVE_WALLET, schemas.WalletState)
initial_wallet_state = lambda: initial_state(schemas.WalletState.FROZEN_MISSING_USER_VERIFICATION, schemas.WalletState)
initial_user_state = lambda: (initial_state(schemas.UserState.CREATED, schemas.UserState), schemas.UserState.CREATED)
initial_loan_state = lambda: initial_state(schemas.LoanApplicationState.DRAFT, schemas.LoanApplicationState)
initial_loan_payment_state = lambda: initial_state(schemas.LoanPaymentState.SCHEDULED, schemas.LoanPaymentState)

def initial_state(initial_value: Enum, enum_type: type):
    _, ret = insert_state(schemas.State(
        state = initial_value,
        enum_type = enum_type,
        next = None,
        previous = None,
        timestamp=datetime.date.today()
    ))
    return ret

""" state utilities """

def insert_state(data: schemas.State) -> Tuple[Timestamp, Any]:
    return state_table.add(asdict(data))

def status_update(data: object, new_state: Enum):
    old_obj = data.get().to_dict()
    old_status = old_obj.get('status')
    _, new_status_ref = state_table.add(asdict(schemas.State(
        state = new_state,
        enum_type = old_obj.get('enum_type'),
        next = None,
        previous = old_status,
        timestamp = datetime.date.today()
    )))
    old_status.update({u'next': new_status_ref})
    data.update({u'status': new_status_ref})

def get_current_state(data_ref: object):
    return data_ref.get().to_dict().get('status')

def traverse_state(state_ref: object, enum_type: type):
    """ Traverse backwards, from the current node to the root """
    return state_ref.get().to_dict().get('previous')

""" firebase utils """

def create_firebase_user():
    return auth.ImportUserRecord(
        uid=fake.uuid4(),
        email=fake.unique.email(),
        password_hash=bytes(fake.password(length=12), 'utf-8'),
        password_salt=bytes(fake.sha1(raw_output=False), 'utf-8')
    )

def import_firebase_users(users):
    hash_alg = auth.UserImportHash.hmac_sha256(key=b'secret_key')
    try:
        result = auth.import_users(users, hash_alg=hash_alg)
        print('Successfully imported {0} users. Failed to import {1} users.'.format(
            result.success_count, result.failure_count))
        for err in result.errors:
            print('Failed to import {0} due to {1}'.format(users[err.index].uid, err.reason))
    except exceptions.FirebaseError as e:
        print(f'Unrecoverable error: {e}')

""" wallet utils """

def insert_internal_wallet(wallet: schemas.Wallet) -> Tuple[Timestamp, Any]:
    assert wallet.wallet_type == schemas.WalletType.INTERNAL_ONLY.value
    return wallet_table.add(asdict(wallet))

def insert_new_wallet_for_user(wallet: schemas.Wallet, user: schemas.User):
    _, wallet_ref = wallet_table.add(asdict(wallet))
    user.update({u'wallets': firestore.ArrayUnion([wallet_ref])})
    return _, wallet_ref

""" entity inserts """

def insert_user(user: schemas.User) -> Tuple[Timestamp, Any]:
    return user_table.add(asdict(user))

""" gather data for output """

def get_all_users():
    return user_table.stream()

def get_user_created_date(user: schemas.User) -> datetime.datetime:
    pass

def get_user_validated_date(user: schemas.User) -> datetime.datetime:
    pass
