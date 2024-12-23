import pytest
from blsttc import SecretKey, SecretKeySet, PublicKey

def test_simple_signature():
    """Test basic signature creation and verification."""
    # Create a new secret key
    sk = SecretKey()
    
    # Get the corresponding public key
    pk = sk.public_key()
    
    # Sign a message
    message = b"Hello, BLS!"
    signature = sk.sign(message)
    
    # Verify the signature
    assert pk.verify(signature, message)

def test_threshold_signatures():
    """Test threshold signature scheme creation and key sharing."""
    # Create a threshold signature scheme with threshold 2
    # This means we need 3 shares to reconstruct a signature (threshold + 1)
    sks = SecretKeySet(2)
    pks = sks.public_keys()
    
    # Verify threshold value
    assert sks.threshold() == 2
    
    # Get individual key shares
    sk_share0 = sks.secret_key_share(0)
    sk_share1 = sks.secret_key_share(1)
    sk_share2 = sks.secret_key_share(2)
    
    # Get corresponding public key shares
    pk_share0 = pks.public_key_share(0)
    pk_share1 = pks.public_key_share(1)
    pk_share2 = pks.public_key_share(2)
    
    # Test that each share can sign and verify
    message = b"Test threshold signature"
    for i, (sk_share, pk_share) in enumerate([
        (sk_share0, pk_share0),
        (sk_share1, pk_share1),
        (sk_share2, pk_share2)
    ]):
        signature = sk_share.sign(message)
        assert pk_share.verify(signature, message), f"Share {i} failed verification"

def test_encryption():
    """Test basic encryption and decryption."""
    # Create a key pair
    sk = SecretKey()
    pk = sk.public_key()
    
    # Test with various message sizes
    messages = [
        b"Short message",
        b"Medium length message with some extra content",
        b"A" * 1000  # Long message
    ]
    
    for message in messages:
        # Encrypt message
        ciphertext = pk.encrypt(message)
        
        # Verify ciphertext is different from message
        assert bytes(ciphertext) != message
        assert len(ciphertext) > 0

def test_derived_keys():
    """Test key derivation functionality."""
    # Create a master key
    master_sk = SecretKey()
    master_pk = master_sk.public_key()
    
    # Test multiple derivations
    child_indices = [b"child_1", b"child_2", b"child_3"]
    
    for index in child_indices:
        # Derive child key
        child_sk = master_sk.derive_child(index)
        child_pk = child_sk.public_key()
        
        # Sign with both keys
        message = b"Test message"
        master_sig = master_sk.sign(message)
        child_sig = child_sk.sign(message)
        
        # Verify signatures
        assert master_pk.verify(master_sig, message), "Master key verification failed"
        assert child_pk.verify(child_sig, message), "Child key verification failed"
        
        # Verify cross-verification fails
        assert not child_pk.verify(master_sig, message), "Cross verification should fail"
        assert not master_pk.verify(child_sig, message), "Cross verification should fail"

def test_threshold_encryption():
    """Test threshold encryption and decryption."""
    # Create a threshold encryption scheme with threshold 2
    sks = SecretKeySet(2)
    pks = sks.public_keys()
    
    # Test messages of different lengths
    messages = [
        b"Short secret",
        b"This is a longer secret message that requires multiple parties to decrypt!",
        b"A" * 1000  # Long message
    ]
    
    for message in messages:
        # Encrypt with master public key
        ciphertext = bytes(pks.public_key().encrypt(message))
        
        # Get decryption shares from different parties
        shares = []
        for i in range(1, 4):  # We need threshold + 1 = 3 shares
            share = sks.decrypt_share(i, ciphertext)
            shares.append((i, share))
        
        # Combine shares to decrypt
        decrypted = bytes(pks.decrypt(shares, ciphertext))
        assert decrypted == message, f"Decryption failed for message of length {len(message)}"

def test_share_handling():
    """Test share handling in threshold encryption."""
    sks = SecretKeySet(2)
    pks = sks.public_keys()
    
    # Test that we need exactly threshold + 1 shares
    message = b"Test message"
    ciphertext = bytes(pks.public_key().encrypt(message))
    
    # Try with too few shares
    shares = [
        (1, sks.decrypt_share(1, ciphertext)),
        (2, sks.decrypt_share(2, ciphertext))
    ]
    with pytest.raises(Exception):
        pks.decrypt(shares, ciphertext)
    
    # Try with out of order shares
    shares = [
        (2, sks.decrypt_share(2, ciphertext)),
        (1, sks.decrypt_share(1, ciphertext)),
        (3, sks.decrypt_share(3, ciphertext))
    ]
    # This should work even with out of order shares
    decrypted = bytes(pks.decrypt(shares, ciphertext))
    assert decrypted == message, "Decryption failed with out of order shares"
    
    # Test with different valid share combinations
    share_combinations = [
        [(1, sks.decrypt_share(1, ciphertext)), 
         (2, sks.decrypt_share(2, ciphertext)), 
         (3, sks.decrypt_share(3, ciphertext))],
        [(1, sks.decrypt_share(1, ciphertext)), 
         (3, sks.decrypt_share(3, ciphertext)), 
         (4, sks.decrypt_share(4, ciphertext))],
        [(2, sks.decrypt_share(2, ciphertext)), 
         (3, sks.decrypt_share(3, ciphertext)), 
         (4, sks.decrypt_share(4, ciphertext))]
    ]
    
    for shares in share_combinations:
        decrypted = bytes(pks.decrypt(shares, ciphertext))
        assert decrypted == message, "Decryption failed with valid share combination"

def test_serialization():
    """Test serialization and deserialization of keys and shares."""
    # Test secret key serialization
    sk = SecretKey()
    sk_bytes = bytes(sk.to_bytes())
    sk_restored = SecretKey.from_bytes(sk_bytes)
    
    # Verify restored key works
    message = b"Test serialization"
    signature = sk.sign(message)
    assert sk_restored.public_key().verify(signature, message)
    
    # Test public key serialization
    pk = sk.public_key()
    pk_bytes = bytes(pk.to_bytes())
    pk_restored = PublicKey.from_bytes(pk_bytes)
    
    # Verify restored public key works
    assert pk_restored.verify(signature, message)

if __name__ == "__main__":
    pytest.main([__file__])
