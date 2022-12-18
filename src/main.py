from typing import List
import schemas
import utils
import random

# seed users and create wallets for each user

def seed_wallet_status():
    _, unfrozen = utils.insert_wallet_status(schemas.WalletStatus(is_frozen=False, frozen_reason_code=None))
    _, missing_user_verification = utils.insert_wallet_status(schemas.WalletStatus(is_frozen=True, frozen_reason_code=101))
    _, fraud_suspected = utils.insert_wallet_status(schemas.WalletStatus(is_frozen=True, frozen_reason_code=102))
    _, staked_for_loan = utils.insert_wallet_status(schemas.WalletStatus(is_frozen=True, frozen_reason_code=103))
    return {
        "unfrozen": unfrozen,
        "missing_user_verification": missing_user_verification,
        "fraud_suspected": fraud_suspected,
        "staked_for_loan": staked_for_loan
    }

def seed_users(wallet_status: List[schemas.WalletStatus], count_users: int):
    for i in range(count_users):
        _, cur_user = utils.insert_user(schemas.User(uid=str(i)))
        utils.insert_wallet(schemas.Wallet(
            wallet_type=3,
            address=random.random(),
            key=random.random(),
            wallet_status=wallet_status["unfrozen"]
        ))

# seed loans and create stake/payment data for each laon

def seed_loans(users: List[schemas.User], count_loans: int, stakes_per_loan: int):
    cur_loan = None

    seed_stakes(cur_loan)
    seed_payments(cur_loan)

def seed_stakes(loan: schemas.Loan):
    pass

def seed_payments(loan: schemas.Loan):
    pass

if __name__ == "__main__":

    COUNT_USERS = 100
    COUNT_LOANS = 50
    STAKES_PER_LOAN = 10

    # todo: delete test data if command line arg is provided

    wallet_status = seed_wallet_status()
    users = seed_users(wallet_status, COUNT_USERS)
    loans = seed_loans(users, COUNT_LOANS, STAKES_PER_LOAN)
