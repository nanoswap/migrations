from typing import List
import schemas
import crud
import nano
import random
import datetime

# seed users and create wallets for each user

def seed_users(count_users: int):
    users_added = []
    for i in range(count_users):

        # create user
        _, cur_user = crud.insert_user(schemas.User(
            uid=str(i),
            status=schemas.UserStatus(
                state=schemas.UserState.CREATED,
                is_frozen=False,
                next=None,
                previous=None,
                timestamp=datetime.date.today()
        )))

        # create wallet for that user
        crud.insert_wallet(schemas.Wallet(
            owner=cur_user,
            wallet_type=schemas.WalletType.WITHDRAW_OR_DEPOSIT,
            address=nano.get_address(),
            key=None,
            status=schemas.WalletStatus(
                state=schemas.WalletState.FROZEN_MISSING_USER_VERIFICATION,
                is_frozen=True,
                next=None,
                previous=None,
                timestamp=datetime.date.today()
            )
        ))

        users_added.append(cur_user)
    
    return users_added

# seed loans and create stake/payment data for each loan

def seed_loans(users: List[schemas.User], count_loans: int, stakes_per_loan: int):
    for i in range(count_loans):

        _, cur_loan = crud.insert_loan(schemas.Loan(
            principal_in_xno=random(),
            start_date=datetime.date.today(),
            monthly_payment=random(),
            number_of_payment_periods=random(),
            status=schemas.LoanApplicationStatus(
                state=schemas.LoanApplicationState.DRAFT,
                next=None,
                previous=None,
                timestamp=datetime.date.today()
            ),
            payment_wallet=schemas.Wallet(),
            principal_wallet=schemas.Wallet(),
            borrower=schemas.User()
        ))

#     seed_stakes(cur_loan)
#     seed_payments(cur_loan)

# def seed_stakes(loan: schemas.Loan):
#     pass

# def seed_payments(loan: schemas.Loan):
#     pass

if __name__ == "__main__":

    COUNT_USERS = 3
    COUNT_LOANS = 5
    STAKES_PER_LOAN = 3

    users = seed_users(COUNT_USERS)
    loans = seed_loans(users, COUNT_LOANS, STAKES_PER_LOAN)
