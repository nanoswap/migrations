from nanoblocks.network import NanoNetwork

network = NanoNetwork()

def get_address() -> str:
    # https://github.com/ipazc/nanoblocks
    wallet = network.wallets.create()
    return ' '.join(wallet.mnemonic)
