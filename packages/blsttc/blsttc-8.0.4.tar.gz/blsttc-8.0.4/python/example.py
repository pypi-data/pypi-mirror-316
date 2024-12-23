from blsttc import SecretKey, PublicKey, SecretKeySet

def test_simple_signature():
    # Create a new secret key
    sk = SecretKey()
    
    # Get the corresponding public key
    pk = sk.public_key()
    
    # Sign a message
    message = b"Hello, BLS!"
    signature = sk.sign(message)
    
    # Verify the signature
    assert pk.verify(signature, message)
    print("Simple signature test passed!")

def test_threshold_signatures():
    # Create a threshold signature scheme with threshold 2
    # This means we need 3 shares to reconstruct a signature (threshold + 1)
    sks = SecretKeySet(2)
    pks = sks.public_keys()
    
    # Get individual key shares
    sk_share0 = sks.secret_key_share(0)
    sk_share1 = sks.secret_key_share(1)
    sk_share2 = sks.secret_key_share(2)
    
    # Get corresponding public key shares
    pk_share0 = pks.public_key_share(0)
    pk_share1 = pks.public_key_share(1)
    pk_share2 = pks.public_key_share(2)
    
    print("Threshold signature scheme created!")
    print(f"Threshold: {sks.threshold()}")

def test_encryption():
    # Create a key pair
    sk = SecretKey()
    pk = sk.public_key()
    
    # Encrypt a message
    message = b"Secret message!"
    ciphertext = pk.encrypt(message)
    
    print("Encryption test completed!")
    print(f"Ciphertext length: {len(ciphertext)} bytes")

def test_derived_keys():
    # Create a master key
    master_sk = SecretKey()
    
    # Derive child keys
    child_index = b"child_1"
    child_sk = master_sk.derive_child(child_index)
    
    # Get corresponding public keys
    master_pk = master_sk.public_key()
    child_pk = child_sk.public_key()
    
    # Sign with both keys
    message = b"Test message"
    master_sig = master_sk.sign(message)
    child_sig = child_sk.sign(message)
    
    # Verify signatures
    assert master_pk.verify(master_sig, message)
    assert child_pk.verify(child_sig, message)
    print("Derived keys test passed!")

def test_threshold_encryption():
    print("\nTesting threshold encryption...")
    
    # Create a threshold encryption scheme with threshold 2
    # This means we need 3 shares to decrypt (threshold + 1)
    sks = SecretKeySet(2)
    pks = sks.public_keys()
    print(f"Created threshold scheme with threshold {sks.threshold()}")
    
    # Create a message and encrypt it with the master public key
    message = b"This is a secret message that requires multiple parties to decrypt!"
    print(f"Original message: {message}")
    
    ciphertext = bytes(pks.public_key().encrypt(message))
    print(f"Encrypted message length: {len(ciphertext)} bytes")
    
    # Get decryption shares from different parties
    # We'll use parties 1, 2, and 3 (need threshold + 1 = 3 parties)
    shares = []
    for i in [1, 2, 3]:
        print(f"Getting decryption share from party {i}")
        share = sks.decrypt_share(i, ciphertext)
        shares.append((i, share))
    print(f"Collected {len(shares)} decryption shares")
    
    # Combine the shares to decrypt the message
    print("Combining shares to decrypt...")
    decrypted = bytes(pks.decrypt(shares, ciphertext))
    print(f"Decrypted message: {decrypted}")
    print(f"Original message: {message}")
    
    assert decrypted == message
    print("Threshold encryption test passed!")

def test_deterministic_keys():
    # Create a deterministic key from bytes
    seed = bytes([i for i in range(32)])  # A predictable sequence for testing
    sk1 = SecretKey.from_bytes(seed)
    pk1 = sk1.public_key()
    
    # Creating another key with the same bytes should give the same key pair
    sk2 = SecretKey.from_bytes(seed)
    pk2 = sk2.public_key()
    
    assert sk1.to_bytes() == sk2.to_bytes()
    assert pk1.to_bytes() == pk2.to_bytes()
    
    print("Deterministic key generation test passed!")

if __name__ == "__main__":
    print("Running BLS signature tests...")
    test_simple_signature()
    test_threshold_signatures()
    test_encryption()
    test_derived_keys()
    test_deterministic_keys()
    test_threshold_encryption()
    print("All tests completed successfully!")
