from typing import List
import schemas
import crud
import nano
import random
import datetime
from datetime import date
import numpy as np

# seed users and create wallets for each user

def seed_users(count_users: int):
    users_added = []

    firebase_users = [crud.create_firebase_user(i) for i in range(count_users)]
    crud.import_firebase_users(firebase_users)

    for i in range(count_users):

        # create user
        _, cur_user = crud.insert_user(schemas.User(
            uid=firebase_users[i].uid,
            status=crud.initial_user_state()
        ))

        # create wallet for user
        personal_wallet = schemas.Wallet(
            wallet_type=schemas.WalletType.WITHDRAW_OR_DEPOSIT,
            address=nano.get_address(),
            status=crud.initial_wallet_state()
        )

        # add new wallet to user
        crud.insert_new_wallet_for_user(personal_wallet, cur_user)
        users_added.append(cur_user)
    
    return users_added

# seed loans and create stake/payment data for each loan

def seed_loans(users: List[schemas.User], count_loans: int):

    loans = []

    for i in range(count_loans):

        # choose a random borrower
        assert len(users) > 0
        borrower = random.sample(users, 1)[0]

        # create wallets
        internal_wallet = schemas.Wallet(
            wallet_type=schemas.WalletType.INTERNAL_ONLY,
            address=nano.get_address(),
            status=crud.active_wallet_state()
        )

        bill_pay_wallet = schemas.Wallet(
            wallet_type=schemas.WalletType.DEPOSIT_ONLY,
            address=nano.get_address(),
            status=crud.active_wallet_state()
        )

        _, internal_wallet_ref = crud.insert_internal_wallet(internal_wallet)
        _, bill_pay_wallet_ref = crud.insert_new_wallet_for_user(bill_pay_wallet, borrower)

        # create the loan
        amount = random.sample(range(10, 100, 5), 1)[0]
        payment_periods = random.sample(range(5, 50, 5), 1)[0]
        monthly_interest = random.sample(list(np.arange(1.05,1.20,0.05)), 1)[0]
        monthly_payment = (amount / payment_periods) * monthly_interest
        start_date = date.today()
        _, cur_loan = crud.insert_loan(schemas.Loan(
            principal_in_xno=amount,
            start_date=start_date,
            monthly_payment=monthly_payment,
            monthly_interest_rate=monthly_interest,
            number_of_payment_periods=payment_periods,
            payment_wallet=bill_pay_wallet_ref,
            principal_wallet=internal_wallet_ref,
            borrower=borrower,
            status=crud.initial_loan_state()
        ))

        # only seed payments for loans that are transitioned to stake?
        # seed_payments(cur_loan, monthly_payment, payment_periods, start_date)

        loans.append(cur_loan)
    
    return loans

def setup_states(objects: List[object], states: dict):
    assert len(objects) == sum(states.values())

    # iterate each state
    count = 0
    for state in states:

        # create n object status' in each state
        for _ in range(states[state]):
            crud.status_update(objects[count], state)
            count += 1

def seed_stakes(loan: schemas.Loan):
    pass

# def seed_payments(loan: schemas.Loan):
#     pass

if __name__ == "__main__":

    user_states = {
        schemas.UserState.CREATED: 10,
        schemas.UserState.VALIDATION_IN_PROGRESS: 10,
        schemas.UserState.VALIDATION_FAILED: 10,
        schemas.UserState.ACTIVE: 10,
        schemas.UserState.FROZEN: 10
    }

    wallet_states = {
        schemas.WalletState.FROZEN_MISSING_USER_VERIFICATION: 10,
        schemas.WalletState.FROZEN_STAKED_FOR_LOAN: 10,
        schemas.WalletState.FROZEN_FRAUD_SUSPECTED: 10,
        schemas.WalletState.VALID_ACTIVE_WALLET: 10
    }

    loan_states = {
        schemas.LoanApplicationState.DRAFT: 10,
        schemas.LoanApplicationState.WITHDRAWN: 10,
        schemas.LoanApplicationState.COLLECTING_STAKE: 10,
        schemas.LoanApplicationState.IN_PROGRESS: 10,
        schemas.LoanApplicationState.FULLY_FUNDED: 10,
        schemas.LoanApplicationState.COMPLETE: 10,
        schemas.LoanApplicationState.DEFAULT: 10
    }

    loan_payment_states = {
        schemas.LoanPaymentState.SCHEDULED: 10,
        schemas.LoanPaymentState.UPCOMING: 10,
        schemas.LoanPaymentState.COMPLETED_ON_TIME: 10,
        schemas.LoanPaymentState.COMPLETED_LATE: 10,
        schemas.LoanPaymentState.LATE: 10,
        schemas.LoanPaymentState.MISSED: 10
    }

    COUNT_USERS = sum(user_states.values())
    COUNT_LOANS = sum(loan_states.values())

    # get total amount to stake?
    # create callback function on state transition and create
    #    stake when transitioning to the fully funded state?
    FULLY_STAKED_LOANS = \
        loan_states[schemas.LoanApplicationState.FULLY_FUNDED] + \
        loan_states[schemas.LoanApplicationState.IN_PROGRESS] + \
        loan_states[schemas.LoanApplicationState.COMPLETE] + \
        loan_states[schemas.LoanApplicationState.DEFAULT]
    
    PARTIALLY_STAKED_LOANS = \
        loan_states[schemas.LoanApplicationState.COLLECTING_STAKE]

    users = seed_users(COUNT_USERS)
    setup_states(users, user_states)
    loans = seed_loans(users, COUNT_LOANS)
    setup_states(loans, loan_states)
    # verified_users = complete_user_verification(users, COUNT_VERIFIED_USERS)
