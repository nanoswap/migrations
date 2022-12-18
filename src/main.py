from typing import List
import schemas
import utils
import random
import datetime

# seed users and create wallets for each user

def seed_users(count_users: int):
    for i in range(count_users):
        _, cur_user = utils.insert_user(schemas.User(uid=str(i)))
        utils.insert_wallet(schemas.Wallet(
            owner=cur_user,
            wallet_type=schemas.WalletType.WITHDRAW_OR_DEPOSIT,
            address="123",
            key=None,
            status=schemas.WalletStatus(
                state=schemas.WalletState.FROZEN_MISSING_USER_VERIFICATION,
                is_frozen=True,
                next=None,
                previous=None,
                timestamp=datetime.datetime.date()
            )
        ))

# seed loans and create stake/payment data for each laon

# def seed_loans(users: List[schemas.User], count_loans: int, stakes_per_loan: int):
#     cur_loan = None

#     seed_stakes(cur_loan)
#     seed_payments(cur_loan)

# def seed_stakes(loan: schemas.Loan):
#     pass

# def seed_payments(loan: schemas.Loan):
#     pass

if __name__ == "__main__":

    COUNT_USERS = 10
    COUNT_LOANS = 5
    STAKES_PER_LOAN = 3

    users = seed_users(COUNT_USERS)
    # loans = seed_loans(users, COUNT_LOANS, STAKES_PER_LOAN)
