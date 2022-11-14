from bitcoinlib.wallets import Wallet as BitcoinLib, wallets_list, wallet_exists, wallet_delete, WalletError, wallet_empty
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey
from bitcoinlib.values import Value


class Wallet:

    # Get a list of all generated wallets
    @staticmethod
    def wallets_list():
        try:
            return wallets_list()
        except (WalletError, Exception) as error:
            return str(error)

    # Check if a wallet exists by name
    @staticmethod
    def wallet_exists(wallet_name):
        try:
            return wallet_exists(wallet_name)
        except (WalletError, Exception) as error:
            return str(error)

    # Class constructor
    def __init__(self, wallet_name, db_uri=None, witness_type='legacy', network='bitcoin', scheme='bip32'):
        self.wallet = None
        self.name = wallet_name
        self.db_uri = db_uri
        self.witness_type = witness_type
        self.network = network
        self.scheme = scheme

    # Create a new wallet
    def create(self, wordlist='english', passphrase_strength=128, passphrase=None):
        try:
            if Wallet.wallet_exists(self.name):
                raise WalletError('Wallet' + self.name + ' already exists.')
            else:
                passphrase = ' '.join(passphrase) if passphrase else Mnemonic(wordlist).generate(passphrase_strength)
                seed = Mnemonic().to_seed(passphrase).hex()
                hdkey = HDKey.from_seed(seed, network=self.network)
                self.wallet = BitcoinLib.create(self.name, hdkey, network=self.network,
                                                scheme=self.scheme, witness_type=self.witness_type, db_uri=self.db_uri)
                return passphrase
        except (WalletError, Exception) as error:
            return str(error)

    # Restore wallet with mnemonic
    def restore(self, passphrase):
        try:
            return self.create(passphrase=passphrase)
        except (WalletError, Exception) as error:
            return str(error)

    # Open an existing wallet
    def open(self):
        try:
            if Wallet.wallet_exists(self.name):
                self.wallet = BitcoinLib(self.name, db_uri=self.db_uri)
                return True
            else:
                raise WalletError('Wallet' + self.name + ' not found.')
        except (WalletError, Exception) as error:
            return str(error)

    # Clear wallet (removes all transactions and generated addresses from this wallet)
    def clear(self):
        try:
            if (self.wallet):
                if wallet_empty(self.name):
                    return True
                else:
                    raise WalletError('Wallet could not be cleared.')
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)

    # Remove wallet
    def remove(self):
        try:
            if (self.wallet):
                if wallet_delete(self.name, force=True, db_uri=self.db_uri):
                    return True
                else:
                    raise WalletError('Wallet could not be deleted.')
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)

    # Close an open wallet
    def close(self):
        try:
            if (self.wallet):
                self.wallet = self.name = None
                return True
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)

    # Update all transactions and UTXO's for specified wallet
    def update(self):
        try:
            if (self.wallet):
                self.wallet.scan(scan_gap_limit=5)
                return self.wallet.last_updated
            else:
                raise WalletError('No wallet open.')
        except (WalletError, WalletError) as error:
            return str(error)

    # Get wallet info
    def info(self):
        try:
            if (self.wallet):
                self.update()
                return {'id': self.wallet.wallet_id, 'name': self.wallet.name, 'scheme': self.wallet.scheme,
                        'witness': self.wallet.witness_type, 'network': self.wallet.network, 'updated': self.wallet.last_updated}
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)

    # Get a list of all transactions
    def tx(self):
        try:
            if (self.wallet):
                self.update()
                transactions = []
                for key in self.wallet.keys(depth=3, network=self.network, is_active=True):
                    balance = Value.from_satoshi(
                        key.balance, network=self.network).str_unit()
                    transactions.append(
                        {'id': key.id, 'path': key.path, 'address': key.address, 'name': key.name, 'balance': balance})
                return transactions
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)

    # Get total balance
    def balance(self):
        try:
            if (self.wallet):
                self.update()
                balance = 0.0
                for wb in self.wallet._balance_update():
                    balance += float(Value(Value.from_satoshi(wb['balance'], network=wb['network']).str_unit()))
                return balance
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)

    # Get a list of all generated addresses
    def addresses(self):
        try:
            if (self.wallet):
                self.update()
                addresses = []
                for key in self.wallet.keys(depth=3, network=self.network, is_active=True):
                    addresses.append(key.address)
                return addresses
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)

    # Show unused address to receive funds.
    def address(self):
        try:
            if (self.wallet):
                self.update()
                key = self.wallet.get_key(network=self.network, cosigner_id=-1)
                return key.address
            else:
                raise WalletError('No wallet open.')
        except (WalletError, Exception) as error:
            return str(error)
