from nanoblocks.network import NanoNetwork
import schemas

network = NanoNetwork()

def get_address() -> str:
    # https://github.com/ipazc/nanoblocks

    # create the wallet, each wallet can store 2^32 accounts
    wallet = network.wallets.create()

    # create the account
    account_0 = wallet.accounts[0]
    # account_0_private_key = account_0.private_key
    

    return ' '.join(wallet.mnemonic)

def test_faucet_deposit(wallet: schemas.Wallet):
    pass

def test_faucet_withdraw(wallet: schemas.Wallet):
    pass

def cleanup_test_wallets():
    pass

def transfer():
    pass
