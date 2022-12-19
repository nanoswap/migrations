from typing import List
import schemas
import crud
import nano
import random
import datetime
from datetime import date

# seed users and create wallets for each user

def seed_users(count_users: int):
    users_added = []
    for i in range(count_users):

        # create user
        _, cur_user = crud.insert_user(schemas.User(
            uid=str(i),
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

def seed_loans(users: List[schemas.User], count_loans: int, stakes_per_loan: int):

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
        _, cur_loan = crud.insert_loan(schemas.Loan(
            principal_in_xno=random.random(),
            start_date=date.today(),
            monthly_payment=random.random(),
            monthly_interest_rate=random.random(),
            number_of_payment_periods=random.random(),
            payment_wallet=bill_pay_wallet_ref,
            principal_wallet=internal_wallet_ref,
            borrower=borrower,
            status=crud.initial_loan_state()
        ))

        loans.append(cur_loan)
    
    return loans

# def complete_user_verification(users: List[schemas.User], count_verified_users: int):
    
#     assert count_verified_users < len(users)

#     # choose which users to verify
#     users_to_verify = random.sample(users, count_verified_users)
#     for user in users_to_verify:
#         crud.verify_user(user)

def seed_stakes(loan: schemas.Loan):
    pass

def seed_payments(loan: schemas.Loan):
    pass

if __name__ == "__main__":

    COUNT_USERS = 3
    COUNT_VERIFIED_USERS = 2
    COUNT_LOANS = 5
    STAKES_PER_LOAN = 3


    users = seed_users(COUNT_USERS)
    loans = seed_loans(users, COUNT_LOANS, STAKES_PER_LOAN)
    # verified_users = complete_user_verification(users, COUNT_VERIFIED_USERS)
