# Simple Bitcoinlib
Simple and lightweight wrapper class for the Bitcoinlib library.

## Installation
See also the [official documentation](https://bitcoinlib.readthedocs.io/en/latest/source/_static/manuals.install.html) of Bitcoinlib
```
pip install bitcoinlib
git clone https://github.com/RootDev4/Crypto-Simple-Bitcoinlib.git
cd Crypto-Simple-Bitcoinlib/
```

## Basic usage
### Static methods
```python
from wallet import Wallet

print(Wallet.wallets_list()) # Get a list of all local wallets
print(Wallet.wallet_exists('foo')) # Check if wallet named 'foo' exists
```

### Create a new wallet
```python
from wallet import Wallet

w = Wallet('name-of-new-wallet')
w.create()

"""
Optional parameters with default values:
   wordlist='english' (Wordlist pool for mnemonic generation)
   passphrase_strength=128 (Number of bits for passphrase key)
"""
```
More wordlists to use: https://github.com/1200wd/bitcoinlib/tree/master/bitcoinlib/wordlist

### Restore a wallet with passphrase (mnemonic)
```python
from wallet import Wallet

w = Wallet('name-of-restored-wallet')
w.restore(['gymnasts', 'stabbed', 'concubines', 'obnoxiously', 'therefore', 'raging', 'chaplains', 'nipped', 'panting', 'warlocks', 'peevishly', 'animal'])
```

### Clear wallet
This removes all transactions and generated addresses from this wallet.
```python
from wallet import Wallet

w = Wallet('testwallet')
if w.open():
    w.clear() # returns bool
```

### Close wallet
```python
from wallet import Wallet

w = Wallet('testwallet')
if w.open():
    w.close() # returns bool
```

### Remove wallet
```python
from wallet import Wallet

w = Wallet('testwallet')
if w.open():
    w.remove() # returns bool
```

### Update
Update all transactions and UTXO's for specified wallet. This is done automatically by info(), tx(), balance(), addresses() and address() methods automatically, so no manual execution is required.
```python
from wallet import Wallet

w = Wallet('testwallet')
if w.open():
    w.update() # returns last update timestamp
```

### Send bitcoins
```python
from wallet import Wallet

w = Wallet('testwallet')
if w.open():
    w.send('1zM3QU1dwsk7dekWWnDJjiZqExrqawTri', 200000) # Amount in satoshi
    w.update()

"""
Optional parameters with default values:
   fee=None (Set fee manually, leave empty to calculate fees automatically)
   min_confirms=1 (Minimal confirmation needed for an transaction before it will be included in inputs)
"""
```

### Open and use wallet
```python
from wallet import Wallet

try:
    w = Wallet('testwallet')
    if w.open():
        print('Wallet information:', w.info())
        print('Wallet transactions:', w.tx())
        print('Wallet total balance:', w.balance()) # BTC
        print('All wallet addresses:', w.addresses())
        print('Generate new wallet receiving address:', w.address())
except Exception as e:
    print(e)
```

## Example output
```
Wallet information: {'id': 8, 'name': 'testwallet', 'scheme': 'bip32', 'witness': 'legacy', 'network': <Network: testnet>, 'updated': datetime.datetime(2022, 11, 14, 19, 27, 20, 459302)}
Wallet transactions: [{'id': 92, 'path': "m/44'/0'/0'", 'address': '1EPSEMc7cCFsKXkxStTchoxug4C3GZpg1w', 'name': 'account 0', 'balance': '0.00000000 BTC'}]
Wallet total balance: 0.015956
All wallet addresses: ['1EPSEMc7cCFsKXkxStTchoxug4C3GZpg1w']
Generate new wallet receiving address: 1zM3QU1dwsk7dekWWnDJjiZqExrqawTri
```

## License
[MIT](../blob/master/LICENSE)