from nanolib import generate_seed, generate_account_id

def get_address():
    # https://nanolib.readthedocs.io/en/latest/tutorial.html#creating-an-account
    seed = generate_seed()
    account_id = generate_account_id(seed, 0)
    return account_id
