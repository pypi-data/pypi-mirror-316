# BLSTTC Python Bindings

Python bindings for the BLSTTC (BLS Threshold Token Cryptography) library, providing BLS (Boneh-Lynn-Shacham) signatures and threshold cryptography functionality.

## Installation

```bash
pip install blsttc
```

## Features

- **BLS Signatures**: Create and verify BLS signatures
- **Public Key Encryption**: Encrypt and decrypt messages using BLS public keys
- **Threshold Signatures**: Create threshold signature schemes where t+1 parties must collaborate to sign
- **Threshold Encryption**: Implement threshold encryption where t+1 parties must collaborate to decrypt
- **Derived Keys**: Generate child keys from master keys

## Quick Start

Here's a simple example demonstrating basic signature functionality:

```python
from blsttc import SecretKey

# Create a new secret key
sk = SecretKey()

# Get the corresponding public key
pk = sk.public_key()

# Sign a message
message = b"Hello, BLS!"
signature = sk.sign(message)

# Verify the signature
assert pk.verify(signature, message)
```

## API Reference

### SecretKey

Secret key for signing and deriving child keys.

Methods:
- `new()`: Create a new random secret key
- `sign(message: bytes) -> Signature`: Sign a message
- `public_key() -> PublicKey`: Get the corresponding public key
- `derive_child(index: bytes) -> SecretKey`: Derive a child secret key
- `to_bytes() -> bytes`: Serialize the secret key
- `from_bytes(bytes) -> SecretKey`: Deserialize a secret key

### PublicKey

Public key for signature verification and encryption.

Methods:
- `verify(signature: Signature, message: bytes) -> bool`: Verify a signature
- `encrypt(message: bytes) -> bytes`: Encrypt a message
- `to_bytes() -> bytes`: Serialize the public key
- `from_bytes(bytes) -> PublicKey`: Deserialize a public key

### SecretKeySet

A set of secret keys for threshold schemes.

Methods:
- `new(threshold: int) -> SecretKeySet`: Create a new threshold key set
- `threshold() -> int`: Get the threshold value
- `secret_key_share(index: int) -> SecretKey`: Get a secret key share
- `public_keys() -> PublicKeySet`: Get the corresponding public key set
- `decrypt_share(index: int, ciphertext: bytes) -> DecryptionShare`: Generate a decryption share

### PublicKeySet

A set of public keys for threshold schemes.

Methods:
- `threshold() -> int`: Get the threshold value
- `public_key() -> PublicKey`: Get the master public key
- `public_key_share(index: int) -> PublicKey`: Get a public key share
- `decrypt(shares: List[Tuple[int, DecryptionShare]], ciphertext: bytes) -> bytes`: Combine shares to decrypt

### DecryptionShare

A share of a decrypted ciphertext in threshold encryption.

Methods:
- `to_bytes() -> bytes`: Serialize the decryption share
- `from_bytes(bytes) -> DecryptionShare`: Deserialize a decryption share

## Examples

### Threshold Signatures

```python
from blsttc import SecretKeySet

# Create a threshold signature scheme (threshold = 2)
sks = SecretKeySet(2)
pks = sks.public_keys()

# Get individual key shares
sk_share1 = sks.secret_key_share(1)
sk_share2 = sks.secret_key_share(2)
sk_share3 = sks.secret_key_share(3)

# Get corresponding public key shares
pk_share1 = pks.public_key_share(1)
pk_share2 = pks.public_key_share(2)
pk_share3 = pks.public_key_share(3)
```

### Threshold Encryption

```python
from blsttc import SecretKeySet

# Create a threshold encryption scheme (threshold = 2)
sks = SecretKeySet(2)
pks = sks.public_keys()

# Encrypt a message with the master public key
message = b"Secret message requiring multiple parties to decrypt!"
ciphertext = bytes(pks.public_key().encrypt(message))

# Get decryption shares from different parties
shares = []
for i in [1, 2, 3]:  # We need threshold + 1 = 3 shares
    share = sks.decrypt_share(i, ciphertext)
    shares.append((i, share))

# Combine shares to decrypt the message
decrypted = bytes(pks.decrypt(shares, ciphertext))
assert decrypted == message
```

### Derived Keys

```python
from blsttc import SecretKey

# Create a master key
master_sk = SecretKey()
master_pk = master_sk.public_key()

# Derive child keys
child_index = b"child_1"
child_sk = master_sk.derive_child(child_index)
child_pk = child_sk.public_key()

# Sign with both keys
message = b"Test message"
master_sig = master_sk.sign(message)
child_sig = child_sk.sign(message)

# Verify signatures
assert master_pk.verify(master_sig, message)
assert child_pk.verify(child_sig, message)
```

### Creating Keys from Bytes

You can create deterministic keys by providing specific bytes:

```python
from blsttc import SecretKey
import os

# Create a deterministic key from 32 bytes
seed = os.urandom(32)  # In practice, use a proper seed generation method
sk = SecretKey.from_bytes(seed)
pk = sk.public_key()

# This will always create the same key pair given the same seed bytes
sk2 = SecretKey.from_bytes(seed)
assert sk2.public_key().to_bytes() == pk.to_bytes()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under either of

 * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
   http://www.apache.org/licenses/LICENSE-2.0)
 * MIT license ([LICENSE-MIT](LICENSE-MIT) or
   http://opensource.org/licenses/MIT)

at your option.
