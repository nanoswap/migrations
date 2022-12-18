from typing import List
import schemas

# seed users and create wallets for each user

def seed_users():
    cur_user = None

    wallets = seed_wallets(cur_user)

def seed_wallets(users: schemas.User):
    pass

# seed loans and create stake/payment data for each laon

def seed_loans(users: List[schemas.User], wallets: List[schemas.Wallet]):
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

    users = seed_users(COUNT_USERS)
    loans = seed_loans(users, COUNT_LOANS, STAKES_PER_LOAN)
