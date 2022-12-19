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
        _, cur_user = crud.insert_user(schemas.User(uid=str(i)))
        personal_wallet = schemas.Wallet(
            wallet_type=schemas.WalletType.WITHDRAW_OR_DEPOSIT,
            address=nano.get_address()
        )

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
        internal_loan_liquidity_wallet = schemas.Wallet(
            wallet_type=schemas.WalletType.INTERNAL_ONLY,
            address=nano.get_address()
        )
        bill_pay_wallet = schemas.Wallet(
            wallet_type=schemas.WalletType.DEPOSIT_ONLY,
            address=nano.get_address()
        )

        crud.insert_internal_wallet(internal_loan_liquidity_wallet)
        crud.insert_new_wallet_for_user(bill_pay_wallet, borrower)

        # create the loan
        _, cur_loan = crud.insert_loan(schemas.Loan(
            principal_in_xno=random.random(),
            start_date=date.today(),
            monthly_payment=random.random(),
            monthly_interest_rate=random.random(),
            number_of_payment_periods=random.random(),
            payment_wallet=bill_pay_wallet,
            principal_wallet=internal_loan_liquidity_wallet,
            borrower=borrower
        ))

        loans.append(cur_loan)
    
    return loans

def seed_stakes(loan: schemas.Loan):
    pass

def seed_payments(loan: schemas.Loan):
    pass

if __name__ == "__main__":

    COUNT_USERS = 3
    COUNT_LOANS = 5
    STAKES_PER_LOAN = 3

    users = seed_users(COUNT_USERS)
    loans = seed_loans(users, COUNT_LOANS, STAKES_PER_LOAN)
