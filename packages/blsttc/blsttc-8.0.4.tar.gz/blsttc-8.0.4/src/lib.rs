//! A pairing-based threshold cryptosystem for collaborative decryption and signatures.

// Clippy warns that it's dangerous to derive `PartialEq` and explicitly implement `Hash`, but the
// `blstrs` types don't implement `Hash`, so we can't derive it.
#![allow(clippy::derive_hash_xor_eq)]
#![warn(missing_docs)]

// re-export crates used in our public API.
pub use blstrs;
pub use group;
pub use rand;
pub use serde; // todo: add serde feature flag later.

mod cmp_pairing;
mod convert;
mod into_fr;
mod secret;
mod util;
mod python;

pub mod error;
pub mod poly;
pub mod serde_impl;

use std::borrow::Borrow;
use std::cmp::Ordering;
use std::fmt;
use std::hash::{Hash, Hasher};
use std::ops::{AddAssign, Mul, MulAssign, SubAssign};

use group::{ff::Field, prime::PrimeCurveAffine, Curve, Group};
use hex_fmt::HexFmt;
use pairing::Engine;
use rand::distributions::{Distribution, Standard};
use rand::{rngs::OsRng, Rng, RngCore, SeedableRng};
use rand_chacha::ChaChaRng;
use serde::{Deserialize, Serialize};
use zeroize::Zeroize;

use crate::cmp_pairing::cmp_affine;
use crate::convert::{derivation_index_into_fr, fr_from_bytes, g1_from_bytes, g2_from_bytes};
pub use crate::error::{Error, Result};
pub use crate::into_fr::IntoFr;
use crate::poly::{Commitment, Poly};
use crate::secret::clear_fr;
use crate::util::sha3_256;

pub use blstrs::{Bls12 as PEngine, G1Affine, G1Projective, G2Affine, G2Projective, Scalar as Fr};

/// The size of a secret key's representation in bytes.
pub const SK_SIZE: usize = 32;

/// The size of a key's representation in bytes.
pub const PK_SIZE: usize = 48;

/// The size of a signature's representation in bytes.
pub const SIG_SIZE: usize = 96;

/// The domain separator tag
pub const DST: &[u8; 43] = b"BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_";

/// A public key.
#[derive(Deserialize, Serialize, Copy, Clone, PartialEq, Eq)]
pub struct PublicKey(#[serde(with = "serde_impl::affine")] G1Affine);

impl Hash for PublicKey {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.0.to_compressed().as_ref().hash(state);
    }
}

impl fmt::Debug for PublicKey {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let uncomp = self.0.to_uncompressed();
        write!(f, "PublicKey({:0.10})", HexFmt(uncomp))
    }
}

impl PartialOrd for PublicKey {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for PublicKey {
    fn cmp(&self, other: &Self) -> Ordering {
        cmp_affine(&self.0, &other.0)
    }
}

/// Utility to convert blsttc to blst types
impl From<PublicKey> for G1Affine {
    fn from(item: PublicKey) -> Self {
        item.0
    }
}

/// Utility to convert blsttc to blst types
impl From<G1Affine> for PublicKey {
    fn from(item: G1Affine) -> Self {
        PublicKey(item)
    }
}

/// Utility to convert blsttc to blst types
impl From<PublicKey> for G1Projective {
    fn from(item: PublicKey) -> Self {
        item.0.into()
    }
}

/// Utility to convert blst to blsttc types
impl From<G1Projective> for PublicKey {
    fn from(item: G1Projective) -> Self {
        PublicKey(item.into())
    }
}

/// Utility to compare between blsttc and blst types
impl std::cmp::PartialEq<G1Affine> for PublicKey {
    fn eq(&self, other: &G1Affine) -> bool {
        &self.0 == other
    }
}

/// Utility to compare between blsttc and blst types
impl std::cmp::PartialEq<G1Projective> for PublicKey {
    fn eq(&self, other: &G1Projective) -> bool {
        &G1Projective::from(self.0) == other
    }
}

impl PublicKey {
    // Utility to check if public key is 0, this is a measure to prevent rogue public key attacks
    fn is_zero(&self) -> bool {
        self.0.is_identity().unwrap_u8() == 1
    }

    /// Returns `true` if the signature matches the element of `G2`.
    pub fn verify_g2<H: Into<G2Affine>>(&self, sig: &Signature, hash: H) -> bool {
        !self.is_zero()
            && PEngine::pairing(&self.0, &hash.into())
                == PEngine::pairing(&G1Affine::generator(), &sig.0)
    }

    /// Returns `true` if the signature matches the message.
    pub fn verify<M: AsRef<[u8]>>(&self, sig: &Signature, msg: M) -> bool {
        self.verify_g2(sig, hash_g2(msg))
    }

    /// Encrypts the message using the OS random number generator.
    ///
    /// Uses the `OsRng` by default. To pass in a custom random number generator, use
    /// `encrypt_with_rng()`.
    pub fn encrypt<M: AsRef<[u8]>>(&self, msg: M) -> Ciphertext {
        self.encrypt_with_rng(&mut OsRng, msg)
    }

    /// Encrypts the message.
    pub fn encrypt_with_rng<R: RngCore, M: AsRef<[u8]>>(&self, rng: &mut R, msg: M) -> Ciphertext {
        let r: Fr = Fr::random(rng);
        let u = G1Affine::generator().mul(r).to_affine();
        let v: Vec<u8> = {
            let g = self.0.mul(r);
            xor_with_hash(g.to_affine(), msg.as_ref())
        };
        let w = hash_g1_g2(u, &v).mul(r).to_affine();
        Ciphertext(u, v, w)
    }

    /// Derives a child public key for a given index.
    pub fn derive_child(&self, index: &[u8]) -> Self {
        let index_fr = derivation_index_into_fr(index);
        let mut child_g1 = self.0;
        child_g1.mul_assign(index_fr);
        PublicKey(child_g1)
    }

    /// Returns the key with the given representation, if valid.
    pub fn from_bytes(bytes: [u8; PK_SIZE]) -> Result<Self> {
        let g1 = g1_from_bytes(bytes)?;
        Ok(PublicKey(g1))
    }

    /// Returns a byte string representation of the public key.
    pub fn to_bytes(self) -> [u8; PK_SIZE] {
        self.0.to_compressed()
    }

    /// Deserialize a hex-encoded representation of a `PublicKey` to a `PublicKey` instance.
    pub fn from_hex(hex: &str) -> Result<Self> {
        let pk_bytes = hex::decode(hex)?;
        let pk_bytes: [u8; PK_SIZE] = pk_bytes.try_into().map_err(|_| Error::InvalidBytes)?;
        Self::from_bytes(pk_bytes)
    }

    /// Serialize this `PublicKey` instance to a hex-encoded `String`.
    pub fn to_hex(&self) -> String {
        hex::encode(self.to_bytes())
    }
}

/// A public key share.
#[derive(Deserialize, Serialize, Clone, Copy, PartialEq, Eq, Hash, Ord, PartialOrd)]
pub struct PublicKeyShare(PublicKey);

impl fmt::Debug for PublicKeyShare {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let uncomp = self.0 .0.to_uncompressed();
        write!(f, "PublicKeyShare({:0.10})", HexFmt(uncomp))
    }
}

impl PublicKeyShare {
    /// Returns `true` if the signature matches the element of `G2`.
    pub fn verify_g2<H: Into<G2Affine>>(&self, sig: &SignatureShare, hash: H) -> bool {
        self.0.verify_g2(&sig.0, hash)
    }

    /// Returns `true` if the signature matches the message.
    pub fn verify<M: AsRef<[u8]>>(&self, sig: &SignatureShare, msg: M) -> bool {
        self.0.verify(&sig.0, msg)
    }

    /// Returns `true` if the decryption share matches the ciphertext.
    pub fn verify_decryption_share(&self, share: &DecryptionShare, ct: &Ciphertext) -> bool {
        let Ciphertext(ref u, ref v, ref w) = *ct;
        let hash = hash_g1_g2(*u, v);
        PEngine::pairing(&share.0, &hash) == PEngine::pairing(&(self.0).0, w)
    }

    /// Derives a child public key share for a given index.
    pub fn derive_child(&self, index: &[u8]) -> Self {
        PublicKeyShare(self.0.derive_child(index))
    }

    /// Returns the key share with the given representation, if valid.
    pub fn from_bytes(bytes: [u8; PK_SIZE]) -> Result<Self> {
        Ok(PublicKeyShare(PublicKey::from_bytes(bytes)?))
    }

    /// Returns a byte string representation of the public key share.
    pub fn to_bytes(self) -> [u8; PK_SIZE] {
        self.0.to_bytes()
    }
}

/// A signature.
// Note: Random signatures can be generated for testing.
#[derive(Deserialize, Serialize, Clone, PartialEq, Eq)]
pub struct Signature(#[serde(with = "serde_impl::affine")] G2Affine);

impl PartialOrd for Signature {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Signature {
    fn cmp(&self, other: &Self) -> Ordering {
        cmp_affine(&self.0, &other.0)
    }
}

impl Distribution<Signature> for Standard {
    fn sample<R: Rng + ?Sized>(&self, rng: &mut R) -> Signature {
        Signature(G2Projective::random(rng).to_affine())
    }
}

impl fmt::Debug for Signature {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let uncomp = self.0.to_uncompressed();
        write!(f, "Signature({:0.10})", HexFmt(uncomp))
    }
}

impl Hash for Signature {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.0.to_compressed().hash(state);
    }
}

impl Signature {
    /// Returns `true` if the signature contains an odd number of ones.
    pub fn parity(&self) -> bool {
        let uncomp = self.0.to_uncompressed();
        let xor_bytes: u8 = uncomp.as_ref().iter().fold(0, |result, byte| result ^ byte);
        0 != xor_bytes.count_ones() % 2
    }

    /// Returns the signature with the given representation, if valid.
    pub fn from_bytes(bytes: [u8; SIG_SIZE]) -> Result<Self> {
        let g2 = g2_from_bytes(bytes)?;
        Ok(Signature(g2))
    }

    /// Returns a byte string representation of the signature.
    pub fn to_bytes(&self) -> [u8; SIG_SIZE] {
        self.0.to_compressed()
    }
}

/// A signature share.
// Note: Random signature shares can be generated for testing.
#[derive(Deserialize, Serialize, Clone, PartialEq, Eq, Hash, Ord, PartialOrd)]
pub struct SignatureShare(pub Signature);

impl Distribution<SignatureShare> for Standard {
    fn sample<R: Rng + ?Sized>(&self, rng: &mut R) -> SignatureShare {
        SignatureShare(rng.gen())
    }
}

impl fmt::Debug for SignatureShare {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let uncomp = (self.0).0.to_uncompressed();
        write!(f, "SignatureShare({:0.10})", HexFmt(uncomp))
    }
}

impl SignatureShare {
    /// Returns the signature share with the given representation, if valid.
    pub fn from_bytes(bytes: [u8; SIG_SIZE]) -> Result<Self> {
        Ok(SignatureShare(Signature::from_bytes(bytes)?))
    }

    /// Returns a byte string representation of the signature share.
    pub fn to_bytes(&self) -> [u8; SIG_SIZE] {
        self.0.to_bytes()
    }
}

/// A secret key; wraps a single prime field element. The field element is
/// heap allocated to avoid any stack copying that result when passing
/// `SecretKey`s between stack frames.
///
/// # Serde integration
/// `SecretKey` implements `Deserialize` but not `Serialize` to avoid accidental
/// serialization in insecure contexts. To enable both use the `::serde_impl::SerdeSecret`
/// wrapper which implements both `Deserialize` and `Serialize`.
#[derive(PartialEq, Eq, PartialOrd, Ord, Clone)]
pub struct SecretKey(Fr);

impl Zeroize for SecretKey {
    fn zeroize(&mut self) {
        clear_fr(&mut self.0)
    }
}

impl Drop for SecretKey {
    fn drop(&mut self) {
        self.zeroize();
    }
}

/// Creates a `SecretKey` containing the zero prime field element.
impl Default for SecretKey {
    fn default() -> Self {
        let mut fr = Fr::zero();
        SecretKey::from_mut(&mut fr)
    }
}

impl Distribution<SecretKey> for Standard {
    /// Creates a new random instance of `SecretKey`. If you do not need to specify your own RNG,
    /// you should use the [`SecretKey::random()`](struct.SecretKey.html#method.random) constructor,
    /// which uses [`rand::thread_rng()`](https://docs.rs/rand/0.7.2/rand/fn.thread_rng.html)
    /// internally as its RNG.
    fn sample<R: Rng + ?Sized>(&self, rng: &mut R) -> SecretKey {
        SecretKey(Fr::random(rng))
    }
}

/// A debug statement where the secret prime field element is redacted.
impl fmt::Debug for SecretKey {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("SecretKey").field(&DebugDots).finish()
    }
}

/// Utility to convert blsttc to blst types
impl From<SecretKey> for blstrs::Scalar {
    fn from(item: SecretKey) -> Self {
        item.0
    }
}

/// Utility to compare between blsttc and blst types
impl std::cmp::PartialEq<Fr> for SecretKey {
    fn eq(&self, other: &Fr) -> bool {
        &self.0 == other
    }
}

impl SecretKey {
    /// Creates a new `SecretKey` from a mutable reference to a field element. This constructor
    /// takes a reference to avoid any unnecessary stack copying/moving of secrets (i.e. the field
    /// element). The field element is copied bytewise onto the heap, the resulting `Box` is
    /// stored in the returned `SecretKey`.
    ///
    /// *WARNING* this constructor will overwrite the referenced `Fr` element with zeros after it
    /// has been copied onto the heap.
    pub fn from_mut(fr: &mut Fr) -> Self {
        let sk = SecretKey(*fr);
        clear_fr(fr);
        sk
    }

    /// Creates a new random instance of `SecretKey`.
    ///
    /// If you want to use/define your own random number generator, you should use the constructor:
    /// [`SecretKey::sample()`](struct.SecretKey.html#impl-Distribution<SecretKey>). If you do not
    /// need to specify your own RNG, you should use the
    /// [`SecretKey::random()`](struct.SecretKey.html#method.random) constructor, which uses
    /// [`rand::thread_rng()`](https://docs.rs/rand/0.7.2/rand/fn.thread_rng.html) internally as its
    /// RNG.
    pub fn random() -> Self {
        rand::random()
    }

    /// Creates a new deterministic SecretKey from a seed.
    pub fn from_seed(seed: &[u8]) -> Self {
        let mut rng = ChaChaRng::from_seed(sha3_256(seed));
        rng.sample(Standard)
    }

    /// Returns the matching public key.
    pub fn public_key(&self) -> PublicKey {
        PublicKey((G1Affine::generator() * self.0).to_affine())
    }

    /// Signs the given element of `G2`.
    pub fn sign_g2<H: Into<G2Affine>>(&self, hash: H) -> Signature {
        Signature(hash.into().mul(self.0).to_affine())
    }

    /// Signs the given message.
    pub fn sign<M: AsRef<[u8]>>(&self, msg: M) -> Signature {
        self.sign_g2(hash_g2(msg))
    }

    /// Converts the secret key to big endian bytes
    pub fn to_bytes(&self) -> [u8; SK_SIZE] {
        self.0.to_bytes_be()
    }

    /// Deserialize from big endian bytes
    pub fn from_bytes(bytes: [u8; SK_SIZE]) -> Result<Self> {
        let mut fr = fr_from_bytes(bytes)?;
        Ok(SecretKey::from_mut(&mut fr))
    }

    /// Deserialize a hex-encoded representation of a `SecretKey` to a `SecretKey` instance.
    pub fn from_hex(hex: &str) -> Result<Self> {
        let sk_bytes = hex::decode(hex)?;
        let sk_bytes: [u8; SK_SIZE] = sk_bytes.try_into().map_err(|_| Error::InvalidBytes)?;
        Self::from_bytes(sk_bytes)
    }

    /// Serialize this `SecretKey` instance to a hex-encoded `String`.
    pub fn to_hex(&self) -> String {
        hex::encode(self.to_bytes())
    }

    /// Returns the decrypted text, or `None`, if the ciphertext isn't valid.
    pub fn decrypt(&self, ct: &Ciphertext) -> Option<Vec<u8>> {
        if !ct.verify() {
            return None;
        }
        let Ciphertext(ref u, ref v, _) = *ct;
        let g = u.mul(self.0).to_affine();
        Some(xor_with_hash(g, v))
    }

    /// Generates a non-redacted debug string. This method differs from
    /// the `Debug` implementation in that it *does* leak the secret prime
    /// field element.
    pub fn reveal(&self) -> String {
        format!("SecretKey({:?})", self.0)
    }

    /// Derives a child secret key for a given index.
    pub fn derive_child(&self, index: &[u8]) -> Self {
        let mut index_fr = derivation_index_into_fr(index);
        index_fr.mul_assign(&self.0);
        SecretKey(index_fr)
    }
}

/// A secret key share.
///
/// # Serde integration
/// `SecretKeyShare` implements `Deserialize` but not `Serialize` to avoid accidental
/// serialization in insecure contexts. To enable both use the `::serde_impl::SerdeSecret`
/// wrapper which implements both `Deserialize` and `Serialize`.
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Default)]
pub struct SecretKeyShare(SecretKey);

/// Can be used to create a new random instance of `SecretKeyShare`. This is only useful for testing
/// purposes as such a key has not been derived from a `SecretKeySet`.
impl Distribution<SecretKeyShare> for Standard {
    fn sample<R: Rng + ?Sized>(&self, rng: &mut R) -> SecretKeyShare {
        SecretKeyShare(rng.gen())
    }
}

impl fmt::Debug for SecretKeyShare {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("SecretKeyShare").field(&DebugDots).finish()
    }
}

impl SecretKeyShare {
    /// Creates a new `SecretKeyShare` from a mutable reference to a field element. This
    /// constructor takes a reference to avoid any unnecessary stack copying/moving of secrets
    /// field elements. The field element will be copied bytewise onto the heap, the resulting
    /// `Box` is stored in the `SecretKey` which is then wrapped in a `SecretKeyShare`.
    ///
    /// *WARNING* this constructor will overwrite the pointed to `Fr` element with zeros once it
    /// has been copied into a new `SecretKeyShare`.
    pub fn from_mut(fr: &mut Fr) -> Self {
        SecretKeyShare(SecretKey::from_mut(fr))
    }

    /// Returns the matching public key share.
    pub fn public_key_share(&self) -> PublicKeyShare {
        PublicKeyShare(self.0.public_key())
    }

    /// Signs the given element of `G2`.
    pub fn sign_g2<H: Into<G2Affine>>(&self, hash: H) -> SignatureShare {
        SignatureShare(self.0.sign_g2(hash))
    }

    /// Signs the given message.
    pub fn sign<M: AsRef<[u8]>>(&self, msg: M) -> SignatureShare {
        SignatureShare(self.0.sign(msg))
    }

    /// Returns a decryption share, or `None`, if the ciphertext isn't valid.
    pub fn decrypt_share(&self, ct: &Ciphertext) -> Option<DecryptionShare> {
        if !ct.verify() {
            return None;
        }
        Some(self.decrypt_share_no_verify(ct))
    }

    /// Returns a decryption share, without validating the ciphertext.
    pub fn decrypt_share_no_verify(&self, ct: &Ciphertext) -> DecryptionShare {
        DecryptionShare((ct.0 * (self.0).0).to_affine())
    }

    /// Generates a non-redacted debug string. This method differs from
    /// the `Debug` implementation in that it *does* leak the secret prime
    /// field element.
    pub fn reveal(&self) -> String {
        format!("SecretKeyShare({:?})", (self.0).0)
    }

    /// Derives a child secret key share for a given index.
    pub fn derive_child(&self, index: &[u8]) -> Self {
        SecretKeyShare(self.0.derive_child(index))
    }

    /// Serializes to big endian bytes
    pub fn to_bytes(&self) -> [u8; SK_SIZE] {
        self.0.to_bytes()
    }

    /// Deserializes from big endian bytes
    pub fn from_bytes(bytes: [u8; SK_SIZE]) -> Result<Self> {
        Ok(SecretKeyShare(SecretKey::from_bytes(bytes)?))
    }
}

/// An encrypted message.
#[derive(Deserialize, Serialize, Debug, Clone, PartialEq, Eq)]
pub struct Ciphertext(
    #[serde(with = "serde_impl::affine")] G1Affine,
    Vec<u8>,
    #[serde(with = "serde_impl::affine")] G2Affine,
);

impl Hash for Ciphertext {
    fn hash<H: Hasher>(&self, state: &mut H) {
        let Ciphertext(ref u, ref v, ref w) = *self;
        u.to_compressed().as_ref().hash(state);
        v.hash(state);
        w.to_compressed().as_ref().hash(state);
    }
}

impl PartialOrd for Ciphertext {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Ciphertext {
    fn cmp(&self, other: &Self) -> Ordering {
        let Ciphertext(ref u0, ref v0, ref w0) = self;
        let Ciphertext(ref u1, ref v1, ref w1) = other;
        cmp_affine(u0, u1).then(v0.cmp(v1)).then(cmp_affine(w0, w1))
    }
}

impl Ciphertext {
    /// Returns `true` if this is a valid ciphertext. This check is necessary to prevent
    /// chosen-ciphertext attacks.
    pub fn verify(&self) -> bool {
        let Ciphertext(ref u, ref v, ref w) = *self;
        let hash = hash_g1_g2(*u, v);
        PEngine::pairing(&G1Affine::generator(), w) == PEngine::pairing(u, &hash)
    }

    /// Returns byte representation of Ciphertext
    pub fn to_bytes(&self) -> Vec<u8> {
        let Ciphertext(ref u, ref v, ref w) = *self;
        let mut result: Vec<u8> = Default::default();
        result.extend(u.to_compressed().as_ref());
        result.extend(w.to_compressed().as_ref());
        result.extend(v);
        result
    }

    /// Returns the Ciphertext with the given representation, if valid.
    pub fn from_bytes(bytes: &[u8]) -> Result<Self> {
        if bytes.len() < PK_SIZE + SIG_SIZE + 1 {
            return Err(Error::InvalidBytes);
        }

        let mut ubytes: [u8; PK_SIZE] = [0u8; PK_SIZE];
        ubytes.copy_from_slice(&bytes[0..PK_SIZE]);
        let u = g1_from_bytes(ubytes)?;

        let mut wbytes: [u8; SIG_SIZE] = [0u8; SIG_SIZE];
        wbytes.copy_from_slice(&bytes[PK_SIZE..PK_SIZE + SIG_SIZE]);
        let w = g2_from_bytes(wbytes)?;

        let v: Vec<u8> = (bytes[PK_SIZE + SIG_SIZE..]).to_vec();

        Ok(Self(u, v, w))
    }
}

/// A decryption share. A threshold of decryption shares can be used to decrypt a message.
#[derive(Clone, Deserialize, Serialize, PartialEq, Eq)]
pub struct DecryptionShare(#[serde(with = "serde_impl::affine")] G1Affine);

impl Distribution<DecryptionShare> for Standard {
    fn sample<R: Rng + ?Sized>(&self, rng: &mut R) -> DecryptionShare {
        DecryptionShare(G1Projective::random(rng).to_affine())
    }
}

impl Hash for DecryptionShare {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.0.to_compressed().as_ref().hash(state);
    }
}

impl fmt::Debug for DecryptionShare {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_tuple("DecryptionShare").field(&DebugDots).finish()
    }
}

impl DecryptionShare {
    /// Deserializes the share from big endian bytes
    pub fn from_bytes(bytes: [u8; PK_SIZE]) -> Result<Self> {
        let g1 = g1_from_bytes(bytes)?;
        Ok(DecryptionShare(g1))
    }

    /// Serializes the share as big endian bytes
    pub fn to_bytes(&self) -> [u8; PK_SIZE] {
        self.0.to_compressed()
    }
}

/// A public key and an associated set of public key shares.
#[derive(Serialize, Deserialize, Clone, PartialEq, Eq, Ord, PartialOrd)]
pub struct PublicKeySet {
    /// The coefficients of a polynomial whose value at `0` is the "master key", and value at
    /// `i + 1` is key share number `i`.
    commit: Commitment,
}

impl Hash for PublicKeySet {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.commit.hash(state);
    }
}

impl fmt::Debug for PublicKeySet {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.debug_struct("PublicKeySet")
            .field("public_key", &self.public_key())
            .field("threshold", &self.threshold())
            .finish()
    }
}

impl From<Commitment> for PublicKeySet {
    fn from(commit: Commitment) -> PublicKeySet {
        PublicKeySet { commit }
    }
}

impl PublicKeySet {
    /// Returns the threshold `t`: any set of `t + 1` signature shares can be combined into a full
    /// signature.
    pub fn threshold(&self) -> usize {
        self.commit.degree()
    }

    /// Returns the public key.
    pub fn public_key(&self) -> PublicKey {
        PublicKey(self.commit.coeff[0])
    }

    /// Returns the `i`-th public key share.
    pub fn public_key_share<T: IntoFr>(&self, i: T) -> PublicKeyShare {
        let value = self.commit.evaluate(into_fr_plus_1(i));
        PublicKeyShare(PublicKey(value))
    }

    /// Combines the shares into a signature that can be verified with the main public key.
    ///
    /// The validity of the shares is not checked: If one of them is invalid, the resulting
    /// signature also is. Only returns an error if there is a duplicate index or too few shares.
    ///
    /// Validity of signature shares should be checked beforehand, or validity of the result
    /// afterwards:
    ///
    /// ```
    /// # extern crate rand;
    /// #
    /// # use std::collections::BTreeMap;
    /// # use blsttc::SecretKeySet;
    /// #
    /// let sk_set = SecretKeySet::random(3, &mut rand::thread_rng());
    /// let sk_shares: Vec<_> = (0..6).map(|i| sk_set.secret_key_share(i)).collect();
    /// let pk_set = sk_set.public_keys();
    /// let msg = "Happy birthday! If this is signed, at least four people remembered!";
    ///
    /// // Create four signature shares for the message.
    /// let sig_shares: BTreeMap<_, _> = (0..4).map(|i| (i, sk_shares[i].sign(msg))).collect();
    ///
    /// // Validate the signature shares.
    /// for (i, sig_share) in &sig_shares {
    ///     assert!(pk_set.public_key_share(*i).verify(sig_share, msg));
    /// }
    ///
    /// // Combine them to produce the main signature.
    /// let sig = pk_set.combine_signatures(&sig_shares).expect("not enough shares");
    ///
    /// // Validate the main signature. If the shares were valid, this can't fail.
    /// assert!(pk_set.public_key().verify(&sig, msg));
    /// ```
    pub fn combine_signatures<T, I, S: Borrow<SignatureShare>>(
        &self,
        shares: I,
    ) -> Result<Signature>
    where
        I: IntoIterator<Item = (T, S)>,
        T: IntoFr,
    {
        let samples = shares
            .into_iter()
            .map(|(i, share)| (i, G2Projective::from((share.borrow().0).0)));
        Ok(Signature(
            interpolate(self.commit.degree(), samples)?.to_affine(),
        ))
    }

    /// Combines the shares to decrypt the ciphertext.
    pub fn decrypt<'a, T, I>(&self, shares: I, ct: &Ciphertext) -> Result<Vec<u8>>
    where
        I: IntoIterator<Item = (T, &'a DecryptionShare)>,
        T: IntoFr,
    {
        let samples = shares
            .into_iter()
            .map(|(i, share)| (i, G1Projective::from(share.0)));
        let g = interpolate(self.commit.degree(), samples)?.to_affine();
        Ok(xor_with_hash(g, &ct.1))
    }

    /// Derives a child public key set for a given index.
    pub fn derive_child(&self, index: &[u8]) -> Self {
        let index_fr = derivation_index_into_fr(index);
        let child_coeffs: Vec<G1Affine> = self
            .commit
            .coeff
            .iter()
            .map(|coeff| {
                let mut child_coeff = *coeff;
                child_coeff.mul_assign(index_fr);
                child_coeff
            })
            .collect();
        PublicKeySet::from(Commitment::from(child_coeffs))
    }

    /// Serializes to big endian bytes
    pub fn to_bytes(&self) -> Vec<u8> {
        self.commit.to_bytes()
    }

    /// Deserializes from big endian bytes
    pub fn from_bytes(bytes: Vec<u8>) -> Result<Self> {
        let commit = Commitment::from_bytes(bytes)?;
        Ok(PublicKeySet { commit })
    }
}

/// A secret key and an associated set of secret key shares.
#[derive(Clone, PartialEq, Eq)]
pub struct SecretKeySet {
    /// The coefficients of a polynomial whose value at `0` is the "master key", and value at
    /// `i + 1` is key share number `i`.
    poly: Poly,
}

impl From<Poly> for SecretKeySet {
    fn from(poly: Poly) -> SecretKeySet {
        SecretKeySet { poly }
    }
}

impl SecretKeySet {
    /// Creates a set of secret key shares, where any `threshold + 1` of them can collaboratively
    /// sign and decrypt. This constructor is identical to the `SecretKeySet::try_random()` in every
    /// way except that this constructor panics if the other returns an error.
    ///
    /// # Panic
    ///
    /// Panics if the `threshold` is too large for the coefficients to fit into a `Vec`.
    pub fn random<R: Rng>(threshold: usize, rng: &mut R) -> Self {
        SecretKeySet::try_random(threshold, rng)
            .unwrap_or_else(|e| panic!("Failed to create random `SecretKeySet`: {e}"))
    }

    /// Creates a set of secret key shares, where any `threshold + 1` of them can collaboratively
    /// sign and decrypt. This constructor is identical to the `SecretKeySet::random()` in every
    /// way except that this constructor returns an `Err` where the `random` would panic.
    pub fn try_random<R: Rng>(threshold: usize, rng: &mut R) -> Result<Self> {
        Poly::try_random(threshold, rng).map(SecretKeySet::from)
    }

    /// Returns the threshold `t`: any set of `t + 1` signature shares can be combined into a full
    /// signature.
    pub fn threshold(&self) -> usize {
        self.poly.degree()
    }

    /// Returns the `i`-th secret key share.
    pub fn secret_key_share<T: IntoFr>(&self, i: T) -> SecretKeyShare {
        let mut fr = self.poly.evaluate(into_fr_plus_1(i));
        SecretKeyShare::from_mut(&mut fr)
    }

    /// Returns the corresponding public key set. That information can be shared publicly.
    pub fn public_keys(&self) -> PublicKeySet {
        PublicKeySet {
            commit: self.poly.commitment(),
        }
    }

    /// Returns a reference to the polynomial
    pub fn poly(&self) -> &Poly {
        &self.poly
    }

    /// Returns the secret master key.
    pub fn secret_key(&self) -> SecretKey {
        let mut fr = self.poly.evaluate(0);
        SecretKey::from_mut(&mut fr)
    }

    /// Derives a child secret key set for a given index.
    pub fn derive_child(&self, index: &[u8]) -> Self {
        // Equivalent to self.poly.clone() * index_fr;
        // The code here follows the same structure as in PublicKeySet for
        // similarity / symmetry / aesthetics, since Commitment can't be
        // multiplied by Fr the same way Poly can.
        let index_fr = derivation_index_into_fr(index);
        let child_coeffs: Vec<Fr> = self
            .poly
            .coeff
            .iter()
            .map(|coeff| {
                let mut child_coeff = *coeff;
                child_coeff.mul_assign(&index_fr);
                child_coeff
            })
            .collect();
        SecretKeySet::from(Poly::from(child_coeffs))
    }

    /// Serializes to big endian bytes
    pub fn to_bytes(&self) -> Vec<u8> {
        self.poly.to_bytes()
    }

    /// Deserializes from big endian bytes
    pub fn from_bytes(bytes: Vec<u8>) -> Result<Self> {
        let poly = Poly::from_bytes(bytes)?;
        Ok(SecretKeySet { poly })
    }
}

/// Returns a hash of the given message in `G2`.
pub fn hash_g2<M: AsRef<[u8]>>(msg: M) -> G2Affine {
    G2Projective::hash_to_curve(msg.as_ref(), DST, &[]).to_affine()
}

/// Returns a hash of the group element and message, in the second group.
fn hash_g1_g2<M: AsRef<[u8]>>(g1: G1Affine, msg: M) -> G2Affine {
    // If the message is large, hash it, otherwise copy it.
    // TODO: Benchmark and optimize the threshold.
    let mut msg = if msg.as_ref().len() > 64 {
        sha3_256(msg.as_ref()).to_vec()
    } else {
        msg.as_ref().to_vec()
    };
    msg.extend(g1.to_compressed().as_ref());
    hash_g2(&msg)
}

/// Returns the bitwise xor of `bytes` with a sequence of pseudorandom bytes determined by `g1`.
fn xor_with_hash(g1: G1Affine, bytes: &[u8]) -> Vec<u8> {
    let digest = sha3_256(&g1.to_compressed());
    let rng = ChaChaRng::from_seed(digest);
    let xor = |(a, b): (u8, &u8)| a ^ b;
    rng.sample_iter(&Standard).zip(bytes).map(xor).collect()
}

/// Given a list of `t + 1` samples `(i - 1, f(i) * g)` for a polynomial `f` of degree `t`, and a
/// group generator `g`, returns `f(0) * g`.
fn interpolate<C, B, T, I>(t: usize, items: I) -> Result<C>
where
    C: Curve<Scalar = Fr>,
    I: IntoIterator<Item = (T, B)>,
    T: IntoFr,
    B: Borrow<C>,
{
    let samples: Vec<_> = items
        .into_iter()
        .take(t + 1)
        .map(|(i, sample)| (into_fr_plus_1(i), sample))
        .collect();
    if samples.len() <= t {
        return Err(Error::NotEnoughShares {
            current: samples.len(),
            required: t + 1,
        });
    }

    if t == 0 {
        return Ok(*samples[0].1.borrow());
    }

    // Compute the products `x_prod[i]` of all but the `i`-th entry.
    let mut x_prod: Vec<C::Scalar> = Vec::with_capacity(t);
    let mut tmp = C::Scalar::one();
    x_prod.push(tmp);
    for (x, _) in samples.iter().take(t) {
        tmp.mul_assign(x);
        x_prod.push(tmp);
    }
    tmp = C::Scalar::one();
    for (i, (x, _)) in samples[1..].iter().enumerate().rev() {
        tmp.mul_assign(x);
        x_prod[i].mul_assign(&tmp);
    }

    let mut result = C::identity();
    for (mut l0, (x, sample)) in x_prod.into_iter().zip(&samples) {
        // Compute the value at 0 of the Lagrange polynomial that is `0` at the other data
        // points but `1` at `x`.
        let mut denom = C::Scalar::one();
        for (x0, _) in samples.iter().filter(|(x0, _)| x0 != x) {
            let mut diff = *x0;
            diff.sub_assign(x);
            denom.mul_assign(&diff);
        }
        // Can we avoid using unwrap with CtOption? Should always be ok
        // because of `is_none` check.
        let denom_inv = denom.invert();
        if denom_inv.is_none().into() {
            return Err(Error::DuplicateEntry);
        }
        l0.mul_assign(&denom_inv.unwrap());
        result.add_assign(&sample.borrow().mul(l0));
    }
    Ok(result)
}

fn into_fr_plus_1<I: IntoFr>(x: I) -> Fr {
    let mut result = Fr::one();
    result.add_assign(&x.into_fr());
    result
}

/// Type that implements `Debug` printing three dots. This can be used to hide the contents of a
/// field in a `Debug` implementation.
struct DebugDots;

impl fmt::Debug for DebugDots {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "...")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    use eyre::{eyre, Result};
    use rand::{self, distributions::Standard, random, Rng};
    use std::collections::BTreeMap;

    #[test]
    fn test_interpolate() {
        let mut rng = rand::thread_rng();
        for deg in 0..5 {
            println!("deg = {deg}");
            let comm = Poly::random(deg, &mut rng).commitment();
            let mut values = Vec::new();
            let mut x = 0;
            for _ in 0..=deg {
                x += rng.gen_range(1..5);
                values.push((x - 1, G1Projective::from(comm.evaluate(x))));
            }
            let actual = interpolate(deg, values).expect("wrong number of values");
            assert_eq!(comm.evaluate(0), actual.to_affine());
        }
    }

    #[test]
    fn test_simple_sig() -> Result<()> {
        let sk0 = SecretKey::random();
        let sk1 = SecretKey::random();
        let pk0 = sk0.public_key();
        let msg0 = b"Real news";
        let msg1 = b"Fake news";
        assert!(pk0.verify(&sk0.sign(msg0), msg0));
        assert!(!pk0.verify(&sk1.sign(msg0), msg0)); // Wrong key.
        assert!(!pk0.verify(&sk0.sign(msg1), msg0)); // Wrong message.
        Ok(())
    }

    #[test]
    fn test_threshold_sig() -> Result<()> {
        let mut rng = rand::thread_rng();
        let sk_set = SecretKeySet::random(3, &mut rng);
        let pk_set = sk_set.public_keys();
        let pk_master = pk_set.public_key();

        // Make sure the keys are different, and the first coefficient is the main key.
        assert_ne!(pk_master, pk_set.public_key_share(0).0);
        assert_ne!(pk_master, pk_set.public_key_share(1).0);
        assert_ne!(pk_master, pk_set.public_key_share(2).0);

        // Make sure we don't hand out the main secret key to anyone.
        let sk_master = sk_set.secret_key();
        let sk_share_0 = sk_set.secret_key_share(0).0;
        let sk_share_1 = sk_set.secret_key_share(1).0;
        let sk_share_2 = sk_set.secret_key_share(2).0;
        assert_ne!(sk_master, sk_share_0);
        assert_ne!(sk_master, sk_share_1);
        assert_ne!(sk_master, sk_share_2);

        let msg = "Totally real news";

        // The threshold is 3, so 4 signature shares will suffice to recreate the share.
        // note: this tests passing a Vec to ::combine_signatures (instead of BTreeMap)
        let sigs: Vec<(_, _)> = [5, 8, 7, 10]
            .iter()
            .map(|&i| {
                let sig = sk_set.secret_key_share(i).sign(msg);
                (i, sig)
            })
            .collect();

        // Each of the shares is a valid signature matching its public key share.
        for (i, sig) in &sigs {
            assert!(pk_set.public_key_share(*i).verify(sig, msg));
        }

        // Combined, they produce a signature matching the main public key.
        let sig = pk_set.combine_signatures(sigs).expect("signatures match");
        assert!(pk_set.public_key().verify(&sig, msg));

        // A different set of signatories produces the same signature.
        let sigs2: BTreeMap<_, _> = [42, 43, 44, 45]
            .iter()
            .map(|&i| {
                let sig = sk_set.secret_key_share(i).sign(msg);
                (i, sig)
            })
            .collect();

        let sig2 = pk_set.combine_signatures(&sigs2).expect("signatures match");
        assert_eq!(sig, sig2);

        Ok(())
    }

    #[test]
    fn test_simple_enc() {
        let sk_bob: SecretKey = random();
        let sk_eve: SecretKey = random();
        let pk_bob = sk_bob.public_key();
        let msg = b"Muffins in the canteen today! Don't tell Eve!";
        let ciphertext = pk_bob.encrypt(&msg[..]);
        assert!(ciphertext.verify());

        // Bob can decrypt the message.
        let decrypted = sk_bob.decrypt(&ciphertext).expect("invalid ciphertext");
        assert_eq!(msg[..], decrypted[..]);

        // Eve can't.
        let decrypted_eve = sk_eve.decrypt(&ciphertext).expect("invalid ciphertext");
        assert_ne!(msg[..], decrypted_eve[..]);

        // Eve tries to trick Bob into decrypting `msg` xor `v`, but it doesn't validate.
        let Ciphertext(u, v, w) = ciphertext;
        let fake_ciphertext = Ciphertext(u, vec![0; v.len()], w);
        assert!(!fake_ciphertext.verify());
        assert_eq!(None, sk_bob.decrypt(&fake_ciphertext));
    }

    #[test]
    fn test_random_extreme_thresholds() {
        let mut rng = rand::thread_rng();
        let sks = SecretKeySet::random(0, &mut rng);
        assert_eq!(0, sks.threshold());
        assert!(SecretKeySet::try_random(usize::max_value(), &mut rng).is_err());
    }

    #[test]
    fn test_threshold_enc() {
        let mut rng = rand::thread_rng();
        let sk_set = SecretKeySet::random(3, &mut rng);
        let pk_set = sk_set.public_keys();
        let msg = b"Totally real news";
        let ciphertext = pk_set.public_key().encrypt(&msg[..]);

        // The threshold is 3, so 4 signature shares will suffice to decrypt.
        let shares: BTreeMap<_, _> = [5, 8, 7, 10]
            .iter()
            .map(|&i| {
                let dec_share = sk_set
                    .secret_key_share(i)
                    .decrypt_share(&ciphertext)
                    .expect("ciphertext is invalid");
                (i, dec_share)
            })
            .collect();

        // Each of the shares is valid matching its public key share.
        for (i, share) in &shares {
            pk_set
                .public_key_share(*i)
                .verify_decryption_share(share, &ciphertext);
        }

        // Combined, they can decrypt the message.
        let decrypted = pk_set
            .decrypt(&shares, &ciphertext)
            .expect("decryption shares match");
        assert_eq!(msg[..], decrypted[..]);
    }

    /// Some basic sanity checks for the `hash_g2` function.
    #[test]
    fn test_hash_g2() {
        let rng = rand::thread_rng();
        let msg: Vec<u8> = rng.sample_iter(&Standard).take(1000).collect();
        let msg_end0: Vec<u8> = msg.iter().chain(b"end0").cloned().collect();
        let msg_end1: Vec<u8> = msg.iter().chain(b"end1").cloned().collect();

        assert_eq!(hash_g2(&msg), hash_g2(&msg));
        assert_ne!(hash_g2(&msg), hash_g2(&msg_end0));
        assert_ne!(hash_g2(&msg_end0), hash_g2(msg_end1));
    }

    /// Some basic sanity checks for the `hash_g1_g2` function.
    #[test]
    fn test_hash_g1_g2() {
        let mut rng = rand::thread_rng();
        let g0 = G1Projective::random(&mut rng).to_affine();
        let g1 = G1Projective::random(&mut rng).to_affine();
        let msg: Vec<u8> = rng.sample_iter(&Standard).take(1000).collect();
        let msg_end0: Vec<u8> = msg.iter().chain(b"end0").cloned().collect();
        let msg_end1: Vec<u8> = msg.iter().chain(b"end1").cloned().collect();

        assert_eq!(hash_g1_g2(g0, &msg), hash_g1_g2(g0, &msg));
        assert_ne!(hash_g1_g2(g0, &msg), hash_g1_g2(g0, &msg_end0));
        assert_ne!(hash_g1_g2(g0, &msg_end0), hash_g1_g2(g0, msg_end1));
        assert_ne!(hash_g1_g2(g0, &msg), hash_g1_g2(g1, &msg));
    }

    /// Some basic sanity checks for the `hash_bytes` function.
    #[test]
    fn test_xor_with_hash() {
        let mut rng = rand::thread_rng();
        let g0 = G1Projective::random(&mut rng).to_affine();
        let g1 = G1Projective::random(&mut rng).to_affine();
        let xwh = xor_with_hash;
        assert_eq!(xwh(g0, &[0; 5]), xwh(g0, &[0; 5]));
        assert_ne!(xwh(g0, &[0; 5]), xwh(g1, &[0; 5]));
        assert_eq!(5, xwh(g0, &[0; 5]).len());
        assert_eq!(6, xwh(g0, &[0; 6]).len());
        assert_eq!(20, xwh(g0, &[0; 20]).len());
    }

    #[test]
    fn test_from_to_bytes() -> Result<()> {
        let sk: SecretKey = random();
        let sig = sk.sign("Please sign here: ______");
        let pk = sk.public_key();
        let pk2 = PublicKey::from_bytes(pk.to_bytes()).expect("invalid pk representation");
        assert_eq!(pk, pk2);
        let sig2 = Signature::from_bytes(sig.to_bytes()).expect("invalid sig representation");
        assert_eq!(sig, sig2);
        let cipher = sk.public_key().encrypt(b"secret msg");
        let cipher2 =
            Ciphertext::from_bytes(&cipher.to_bytes()).expect("invalid cipher representation");
        assert_eq!(cipher, cipher2);
        Ok(())
    }

    #[test]
    fn test_from_to_hex() -> Result<()> {
        let sk_hex = "4a353be3dac091a0a7e640620372f5e1e2e4401717c1e79cac6ffba8f6905604";
        let sk = SecretKey::from_hex(sk_hex)?;
        let sk2_hex = sk.to_hex();
        let sk2 = SecretKey::from_hex(&sk2_hex)?;
        assert_eq!(sk, sk2);
        let pk_hex = "85695fcbc06cc4c4c9451f4dce21cbf8de3e5a13bf48f44cdbb18e203\
                      8ba7b8bb1632d7911ef1e2e08749bddbf165352";
        let pk = PublicKey::from_hex(pk_hex)?;
        let pk2_hex = pk.to_hex();
        let pk2 = PublicKey::from_hex(&pk2_hex)?;
        assert_eq!(pk, pk2);
        Ok(())
    }

    #[test]
    fn test_serde() -> Result<()> {
        let sk = SecretKey::random();
        let sig = sk.sign("Please sign here: ______");
        let pk = sk.public_key();
        let ser_pk = bincode::serialize(&pk).expect("serialize public key");
        let deser_pk: PublicKey = bincode::deserialize(&ser_pk).expect("deserialize public key");
        assert_eq!(ser_pk.len(), PK_SIZE);
        assert_eq!(pk, deser_pk);
        let ser_sig = bincode::serialize(&sig).expect("serialize signature");
        let deser_sig = bincode::deserialize(&ser_sig).expect("deserialize signature");
        assert_eq!(ser_sig.len(), SIG_SIZE);
        assert_eq!(sig, deser_sig);
        Ok(())
    }

    #[test]
    fn test_zeroize() {
        let zero_sk = SecretKey::from_mut(&mut Fr::zero());
        let mut sk = SecretKey::random();
        assert_ne!(zero_sk, sk);
        sk.zeroize();
        assert_eq!(zero_sk, sk);
    }

    #[test]
    fn test_rng_seed() {
        let sk1 = SecretKey::random();
        let sk2 = SecretKey::random();

        assert_ne!(sk1, sk2);
        let mut seed = [0u8; 32];
        rand::thread_rng().fill_bytes(&mut seed);

        let mut rng = ChaChaRng::from_seed(seed);
        let sk3: SecretKey = rng.sample(Standard);

        let mut rng = ChaChaRng::from_seed(seed);
        let sk4: SecretKey = rng.sample(Standard);
        assert_eq!(sk3, sk4);
    }

    #[test]
    fn test_interoperability() -> Result<()> {
        // This test only pases if fn sign and fn verify are using the BLST code
        // https://github.com/Chia-Network/bls-signatures/blob/ee71adc0efeae3a7487cf0662b7bee3825752a29/src/test.cpp#L249-L260
        let skbytes = [
            74, 53, 59, 227, 218, 192, 145, 160, 167, 230, 64, 98, 3, 114, 245, 225, 226, 228, 64,
            23, 23, 193, 231, 156, 172, 111, 251, 168, 246, 144, 86, 4,
        ];
        let pkbytes = [
            133, 105, 95, 203, 192, 108, 196, 196, 201, 69, 31, 77, 206, 33, 203, 248, 222, 62, 90,
            19, 191, 72, 244, 76, 219, 177, 142, 32, 56, 186, 123, 139, 177, 99, 45, 121, 17, 239,
            30, 46, 8, 116, 155, 221, 191, 22, 83, 82,
        ];
        let msgbytes = [7, 8, 9];
        let sigbytes = [
            184, 250, 166, 214, 163, 136, 28, 159, 219, 173, 128, 59, 23, 13, 112, 202, 92, 191,
            30, 107, 165, 165, 134, 38, 45, 243, 104, 199, 90, 205, 29, 31, 250, 58, 182, 238, 33,
            199, 31, 132, 68, 148, 101, 152, 120, 245, 235, 35, 12, 149, 141, 213, 118, 176, 139,
            133, 100, 170, 210, 238, 9, 146, 232, 90, 30, 86, 95, 41, 156, 213, 58, 40, 93, 231,
            41, 147, 127, 112, 220, 23, 106, 31, 1, 67, 33, 41, 187, 43, 148, 211, 213, 3, 31, 128,
            101, 161,
        ];
        let sk = SecretKey::from_bytes(skbytes)?;
        let pk = sk.public_key();
        // secret key gives same public key
        assert_eq!(pkbytes, pk.to_bytes());
        // signature matches test vector
        let sig = sk.sign(msgbytes);
        assert_eq!(sigbytes, sig.to_bytes());
        // signature can be verified
        assert!(pk.verify(&sig, msgbytes));
        Ok(())
    }

    #[test]
    fn test_sk_to_from_bytes() -> Result<()> {
        use crate::serde_impl::SerdeSecret;
        let sk = SecretKey::random();
        // bincode is little endian, but will always serialize sk to big endian
        let bincode_bytes = bincode::serialize(&SerdeSecret(&sk))?;
        // sk.to_bytes() is big endian
        let sk_be_bytes = sk.to_bytes();
        assert_eq!(bincode_bytes, sk_be_bytes);
        // from bytes gives original secret key
        let restored_sk = SecretKey::from_bytes(sk_be_bytes).expect("invalid sk bytes");
        assert_eq!(sk, restored_sk);
        Ok(())
    }

    #[test]
    fn vectors_sk_to_from_bytes() -> Result<()> {
        // from https://github.com/Chia-Network/bls-signatures/blob/ee71adc0efeae3a7487cf0662b7bee3825752a29/src/test.cpp#L249
        let sk_hex = "4a353be3dac091a0a7e640620372f5e1e2e4401717c1e79cac6ffba8f6905604";
        let pk_hex = "85695fcbc06cc4c4c9451f4dce21cbf8de3e5a13bf48f44cdbb18e2038ba7b8bb1632d7911ef1e2e08749bddbf165352";
        let sk_vec = hex::decode(sk_hex)?;
        let mut sk_bytes = [0u8; SK_SIZE];
        sk_bytes[..SK_SIZE].clone_from_slice(&sk_vec[..SK_SIZE]);
        let sk = SecretKey::from_bytes(sk_bytes).expect("invalid sk bytes");
        let pk = sk.public_key();
        let pk_bytes = pk.to_bytes();
        let pk_to_hex = &format!("{}", HexFmt(&pk_bytes));
        assert_eq!(pk_to_hex, pk_hex);
        Ok(())
    }

    #[test]
    fn test_public_key_set_to_from_bytes_distinctive_properties() {
        let threshold = 3;
        let mut rng = rand::thread_rng();
        let sk_set = SecretKeySet::random(threshold, &mut rng);
        let pk_set = sk_set.public_keys();
        // length is fixed to (threshold + 1) * 48
        let pk_set_bytes = pk_set.to_bytes();
        assert_eq!(pk_set_bytes.len(), (threshold + 1) * PK_SIZE);
        // the first bytes of the public key set match the public key
        let pk = pk_set.public_key();
        let pk_bytes = pk.to_bytes();
        let pk_bytes_size = pk_bytes.len();
        for i in 0..pk_bytes_size {
            assert_eq!(pk_bytes[i], pk_set_bytes[i]);
        }
        // from bytes gives original pk set
        let restored_pk_set =
            PublicKeySet::from_bytes(pk_set_bytes).expect("invalid public key set bytes");
        assert_eq!(pk_set, restored_pk_set);
    }

    #[test]
    fn test_public_key_set_to_from_bytes_threshold_0() {
        // for threshold 0 the public key set matches the public key and all
        // public key shares
        let threshold = 0;
        let mut rng = rand::thread_rng();
        let sk_set = SecretKeySet::random(threshold, &mut rng);
        let pk_set = sk_set.public_keys();
        let pk_set_bytes = pk_set.to_bytes();
        let pk = pk_set.public_key();
        let pk_bytes = pk.to_bytes();
        assert_eq!(pk_set_bytes, pk_bytes);
        let pk_share_0 = pk_set.public_key_share(0);
        let pk_share_0_bytes = pk_share_0.to_bytes();
        assert_eq!(pk_set_bytes, pk_share_0_bytes);
        let pk_share_1 = pk_set.public_key_share(1);
        let pk_share_1_bytes = pk_share_1.to_bytes();
        assert_eq!(pk_set_bytes, pk_share_1_bytes);
    }

    #[test]
    fn vectors_public_key_set_to_from_bytes() -> Result<()> {
        let vectors = vec![
            // Plain old Public Key Set
            vec![
                // public key set
                "b89f8983d73b6ef75f07f90bc5a58d501b9204f9f304fc9354a66271944b25460845b22d3759c2c8889be552ae23617096b5bfcf90273c61ad102f97c66155de2d9eee3b803e83118095d8b0955f177b105371481e8d9b18d8f610a05b94c1cf",
                // public key
                "b89f8983d73b6ef75f07f90bc5a58d501b9204f9f304fc9354a66271944b25460845b22d3759c2c8889be552ae236170",
                // public key share 0
                "a0f7640853a86e68ef7ac705b6f5bdd15bb4656dbe9578b24b2cceb1ee8576646de140a417eb687e7dbe1a1bfff4f5cd",
                // public key share 1
                "8c2e9d7c02fb3ec87548cc2456904899b9d100c798ae2e08461dc8471b907664e38af99701adaaf6b604367ce70a72ce",
                // public key share 2
                "851d512dfbc25d2200982d70b107dad84bfef82d6f9fe9ce9c7bef7917755e3b2e504324ba2b7ed233b77f9c825188e8",
            ],
            // Trailing zero in the Public Key Set
            // This will fail any implementation with little endian shenaigans
            vec![
                "9455aa0495c1b0706507dd09531c71940e4cfeca1d5533dc096f4d5f045ba02f362790486e44e9d4a204938c65bd45208d19e0f29c53f6a1491c5aa24c4095759b57acccf1b801e5ea0270dac3c1e0d24a1058cbc4d8a3f185c1e87cefdaaa00",
                "9455aa0495c1b0706507dd09531c71940e4cfeca1d5533dc096f4d5f045ba02f362790486e44e9d4a204938c65bd4520",
                "881ffed3cc7a51355ffb1a99928ddfa16fb739ee7d4194e94e614ff0144d9978270cd2ffc0d2f95a664d450c4a7890c5",
                "b06db35fe602cbe651667aef2a77f53af1e8a4abb8764cec021d0aeac77728a5accc519bcfb07b609874fa76bd36452c",
                "856bb79f082919dfe2a4601765c2d6094ff122f494db7593a3eab2340136a50d7ad8ba20b09367c6c2b87a543cfee014",
            ],
            // Trailing zero in the Public Key
            vec![
                "afddb9cb9b636f176fd3e4d66ebf1d5e1b8feb0e43723e10fb4e4bc00bbbc3d29d6f6c8d7beca65fee2c89bd54e79e00a151ba6cea3fbe4b84bf14e99ef83edc1a805305ddeb998b93cb30c965abac057bd2dbfd73a00277638ec98da02b770c",
                "afddb9cb9b636f176fd3e4d66ebf1d5e1b8feb0e43723e10fb4e4bc00bbbc3d29d6f6c8d7beca65fee2c89bd54e79e00",
                "af121474a59ff060cb6b7862431cfc4ff6188c88120e0f686c790401d716ea6cd46a08201fcf88a0e96e324fcf08a25f",
                "b7ce6b16cfed4d94e95478902e64920bf95e84848bc471b569c547a4d59265be3865f6f1de40720045446ad9cd15b5ba",
                "a08b1043e38862e9442574d0afd1ed47c197d1dec2f0600edfedbb9e45cfac07095e15ddc8c6b91d0657272bb990d3e7",
            ],
            // Trailing zero in a Public Key Share
            vec![
                "8a4f064135d1a26d71b77f8d3f3a611e8f4de6489afb5b99e567aa6e93ee6a67f1e8fdde8105080382c822a52cf989ad833106149091a207a0e0fd3353e1a2c6dbe0147538a35b562e9b779252e8707c3cd98759a18a1c55cc7eb0f9f8440664",
                "8a4f064135d1a26d71b77f8d3f3a611e8f4de6489afb5b99e567aa6e93ee6a67f1e8fdde8105080382c822a52cf989ad",
                "907ec2454a752d18a172cb7c99d5f7952a558bdbd2675c107aeb84f0281f39cf72022e3ec26d05e86809ee0e2ebe352a",
                "8bd292ce33c1bcec80ce6cf029aeac292d9563d6e718fdcd8573188f88364442f2a8d51f1124b69c48fe5adc77512800",
                "aa4f3dbd12d6184bb5426187e46d20df9c160b4c5f9028b73fc904c988405e8655f1eaf979992a163d03d601f39efce1",
            ]
        ];
        for vector in vectors {
            // read PublicKeyShare from hex
            let pks_bytes = hex::decode(vector[0])?;
            let pks = PublicKeySet::from_bytes(pks_bytes).expect("Invalid public key set bytes");
            // check public key
            let pk = pks.public_key();
            let pk_hex = &format!("{}", HexFmt(&pk.to_bytes()));
            assert_eq!(pk_hex, vector[1]);
            // check public key shares
            let pk_share_0 = pks.public_key_share(0);
            let pk_share_0_hex = &format!("{}", HexFmt(&pk_share_0.to_bytes()));
            assert_eq!(pk_share_0_hex, vector[2]);
            let pk_share_1 = pks.public_key_share(1);
            let pk_share_1_hex = &format!("{}", HexFmt(&pk_share_1.to_bytes()));
            assert_eq!(pk_share_1_hex, vector[3]);
            let pk_share_2 = pks.public_key_share(2);
            let pk_share_2_hex = &format!("{}", HexFmt(&pk_share_2.to_bytes()));
            assert_eq!(pk_share_2_hex, vector[4]);
        }

        Ok(())
    }

    #[test]
    fn test_secret_key_set_to_from_bytes_distictive_properties() {
        let threshold = 3;
        let mut rng = rand::thread_rng();
        let poly = Poly::random(threshold, &mut rng);
        let sk_set = SecretKeySet::from(poly);
        // length is fixed to (threshold + 1) * 32
        let sk_set_bytes = sk_set.to_bytes();
        assert_eq!(sk_set_bytes.len(), (threshold + 1) * SK_SIZE);
        // the first bytes of the secret key set match the secret key
        let sk = sk_set.secret_key();
        let sk_bytes = sk.to_bytes();
        let sk_bytes_size = sk_bytes.len();
        for i in 0..sk_bytes_size {
            assert_eq!(sk_bytes[i], sk_set_bytes[i]);
        }
        // from bytes gives original sk set
        let restored_sk_set =
            SecretKeySet::from_bytes(sk_set_bytes).expect("invalid secret key set bytes");
        // cannot assert_eq! for SecretKeySet so test the secret_key
        // TODO decide if testing the secret key is adequate for testing the
        // entire restored secret key set
        let restored_sk = restored_sk_set.secret_key();
        assert_eq!(sk, restored_sk);
    }

    #[test]
    fn test_secret_key_set_to_from_bytes_threshold_0() {
        // for threshold 0 the secret key set matches the secret key and all
        // secret key shares
        let threshold = 0;
        let mut rng = rand::thread_rng();
        let sk_set = SecretKeySet::random(threshold, &mut rng);
        let sk_set_bytes = sk_set.to_bytes();
        let sk = sk_set.secret_key();
        let sk_bytes = sk.to_bytes();
        assert_eq!(sk_set_bytes, sk_bytes);
        let sk_share_0 = sk_set.secret_key_share(0);
        let sk_share_0_bytes = sk_share_0.to_bytes();
        assert_eq!(sk_set_bytes, sk_share_0_bytes);
        let sk_share_1 = sk_set.secret_key_share(1);
        let sk_share_1_bytes = sk_share_1.to_bytes();
        assert_eq!(sk_set_bytes, sk_share_1_bytes);
    }

    #[test]
    fn vectors_secret_key_set_to_from_bytes() -> Result<()> {
        let vectors = vec![
            // Plain old Secret Key Set
            // Sourced from Poly::reveal and SecretKey::reveal
            vec![
                // secret key set
                "474da5f155b0580b6ffcd28b62973226883bfc75658a06c2592175448221f68f64681c46c8de0e28f0666b6a849463e07a8a353bbd4b01457c0aeeb6e7dd1fa6",
                // secret key
                "474da5f155b0580b6ffcd28b62973226883bfc75658a06c2592175448221f68f",
                // secret key share 0
                "37c81ae4f4f0e8ec2d2965eddd89be01af088dae22d6ac08d52c63fc69ff1634",
                // secret key share 1
                "28428fd8943179ccea55f950587c49dcd5d51ee6e023514f513752b451dc35d9",
                // secret key share 2
                "18bd04cc33720aada7828cb2d36ed5b7fca1b01f9d6ff695cd42416c39b9557e",
            ],
            // Leading byte of Secret Key Set is zero
            // Also covers the Secret Key with a leading zero
            // This will fail for implementations with incorrect padding
            vec![
                "004e7590e4a4a97685f4d9f2c10cd8b71c88fead21f701701ddb2ee9c2d2047f015ea5a4ffc5ae4830f5dae1d0b3fed09b9bbebb983c1fc7d79b351361ba075a",
                "004e7590e4a4a97685f4d9f2c10cd8b71c88fead21f701701ddb2ee9c2d2047f",
                "01ad1b35e46a57beb6eab4d491c0d787b824bd68ba332137f57663fd248c0bd9",
                "030bc0dae4300606e7e08fb66274d65853c07c24526f40ffcd11991086461333",
                "046a667fe3f5b44f18d66a983328d528ef5c3adfeaab60c7a4acce23e8001a8d",
            ],
            // Leading byte of Secret Key Share is zero
            vec![
                "1c838171bcbb0c20e3f259cadcba86e611eb4587f069a6dcd5ee46f186e37039579311c4b4d7d016c3cae22fad69c8b8f5ce17ac826c8fefd6b38b746dd83cf8",
                "1c838171bcbb0c20e3f259cadcba86e611eb4587f069a6dcd5ee46f186e37039",
                "0028ebe347f55eef748363f280827799b3fbb93172d7dacdaca1d266f4bbad30",
                "57bbfda7fccd2f06384e46222dec4052a9c9d0ddf5446abd83555ddb6293ea28",
                "3b616819880781d4c8df5049d1b431064bda448777b29eae5a08e950d06c271f",
            ],
        ];
        for vector in vectors {
            // get parent keypair
            let sks_bytes = hex::decode(vector[0])?;
            let sks = SecretKeySet::from_bytes(sks_bytes).expect("invalid secret key set bytes");
            // check secret key
            let sk = sks.secret_key();
            let sk_hex = &format!("{}", HexFmt(&sk.to_bytes()));
            assert_eq!(sk_hex, vector[1]);
            // check secret key shares
            let sk_share_0 = sks.secret_key_share(0);
            let sk_share_0_hex = &format!("{}", HexFmt(&sk_share_0.to_bytes()));
            assert_eq!(sk_share_0_hex, vector[2]);
            let sk_share_1 = sks.secret_key_share(1);
            let sk_share_1_hex = &format!("{}", HexFmt(&sk_share_1.to_bytes()));
            assert_eq!(sk_share_1_hex, vector[3]);
            let sk_share_2 = sks.secret_key_share(2);
            let sk_share_2_hex = &format!("{}", HexFmt(&sk_share_2.to_bytes()));
            assert_eq!(sk_share_2_hex, vector[4]);
        }

        Ok(())
    }

    #[test]
    fn test_decryption_share_to_from_bytes() {
        let mut rng = rand::thread_rng();
        let sk_set = SecretKeySet::random(3, &mut rng);
        let pk_set = sk_set.public_keys();
        let msg = b"Totally real news";
        let ciphertext = pk_set.public_key().encrypt(&msg[..]);
        let dec_share = sk_set
            .secret_key_share(8)
            .decrypt_share(&ciphertext)
            .expect("ciphertext is invalid");
        let dec_share_bytes = dec_share.to_bytes();
        let restored_dec_share =
            DecryptionShare::from_bytes(dec_share_bytes).expect("invalid decryption share bytes");
        assert_eq!(dec_share, restored_dec_share);
    }

    #[test]
    fn test_derive_child_secret_key() {
        let sk = SecretKey::random();
        // derivation index 0
        let child0 = sk.derive_child(&[0]);
        assert!(child0 != sk);
        // derivation index 00
        let child00 = sk.derive_child(&[0, 0]);
        assert!(child00 != sk);
        assert!(child00 != child0);
        // derivation index 1
        let child1 = sk.derive_child(&[1]);
        assert!(child1 != sk);
        assert!(child1 != child0);
        // derivation index 2
        let child2 = sk.derive_child(&[2]);
        assert!(child2 != sk);
        assert!(child2 != child0);
        assert!(child2 != child1);
        // derivation index 3
        let child3 = sk.derive_child(&[3]);
        assert!(child3 != sk);
        assert!(child3 != child0);
        assert!(child3 != child0);
        assert!(child3 != child1);
        assert!(child3 != child2);
        // very large derivation index can be used, eg 100 bytes
        let index100b = [3u8; 100];
        let child100b = sk.derive_child(&index100b);
        assert!(child100b != sk);
    }

    #[test]
    fn test_derive_child_public_key() {
        let sk = SecretKey::random();
        let pk = sk.public_key();
        // the derived keypair is a match
        let child_sk = sk.derive_child(&[0]);
        let child_pk = pk.derive_child(&[0]);
        assert_eq!(child_pk, child_sk.public_key());
    }

    #[test]
    fn test_derivation_index_into_fr() {
        // index 0 does not give Fr::zero
        let fr_from_0 = derivation_index_into_fr(&[0]);
        assert!(fr_from_0 != Fr::zero());
        // index 1 does not give Fr::one
        let fr_from_1 = derivation_index_into_fr(&[1]);
        assert!(fr_from_1 != Fr::one());
        // index > q gives valid Fr that isn't Fr::MAX
        // the check relies on the fact Fr::MAX + 1 = 0
        let mut fr_from_2pow256 = derivation_index_into_fr(&[255u8; 32]);
        fr_from_2pow256.add_assign(&Fr::one());
        assert!(fr_from_2pow256 != Fr::zero());
    }

    #[test]
    fn test_derive_child_key_vectors() -> Result<()> {
        let vectors = vec![
            // Plain old derivation
            vec![
                // secret key
                "474da5f155b0580b6ffcd28b62973226883bfc75658a06c2592175448221f68f",
                // public key
                "ac378101f72ddf89998b3b20f9498bec1443fb095bbdaa40ad8e0cbc1fe73a147e304a14cce88bc4bd23da1e45eb3742",
                // random index
                "57cb1459985906a9c00036f0b1d700b52a4dc25b3e0ff3808dd2c9fa6ca6ba87",
                // child secret key at random index
                "2125994b85332e1478e7d01b81f30933e92074ff05c873ee8306a43dd5be17d4",
                // child public key at random index
                "a01044f663a75c2000c4b33cec26c92e35c56bb77ed4dc1c1bfe88c890df9caf9153b7069dcf1d93c934ccf391fca3a1",
            ],
            vec![
                // secret key
                "0000000000000000000000000000000000000000000000000000000000000003",
                // public key
                "89ece308f9d1f0131765212deca99697b112d61f9be9a5f1f3780a51335b3ff981747a0b2ca2179b96d2c0c9024e5224",
                // index 0
                "00",
                // child secret key at index 0
                "67b1bb08bee06eaa528d1a412d2d4237daa1204234543f27e0afe901a520b78e",
                // child public key at index 0
                "842de40cbb1d66e60b5e4ce3ce02e6081d5fdacf3dbd1cb0c5959c306d54cab40622c5188f4fa91c818c1a5560bcbcc1",
                // index 1
                "01",
                // child secret key at index 1
                "379446550d351164cf5a8ed4f6ad4cb7cab5c7c3388f103515b84e40aaa1ef30",
                // child public key at index 1
                "aecea20ec775b2fd9640517fa4da8e845217f1b4667ace6e7340d1b35ef986c1603056b4a6a66bebe5d2b5a86ff5a7b5",
                // index 2
                "02",
                // child secret key at index 2
                "1ac3cee2dca114a3d0003e6bcf0ac2da26ec2b28044da4bc550a655b527b4693",
                // child public key at index 2
                "8c9c00407c09dcc6ea186fd8d5e6a39018c83b95ff5610307b6e6b186d00ab925b82405adb120e9c3498b8581a282672",
                // index 1 with left padding
                // different to single byte index "01"
                "0000000000000000000000000000000000000000000000000000000000000001",
                // child secret key for 1 with left padding
                "41308f892e28336c5cbf3109c0a6717e759a68badd217e2816b02acc68a852ad",
                // child public key for 1 with left padding
                "a1be856a26d993fee069481b37b22fd4955fcc5cb289bb30f4c6e98d9c36fd6892c7d36674d400c4bda136f9b7c6e1dc",
                // index 1 with right padding
                // different to single byte index "01"
                "0100000000000000000000000000000000000000000000000000000000000000",
                // child secret key for 1 with right padding
                "48c9761c4350e2cf76a765b7d95e6021902d5daf3221cfe2d687ae3e9fba3717",
                // child public key for 1 with right padding
                "a6b1df11c4346da734253993e329ed54ad99907024f35e555374d46b33fb602790105479e68e0d89c48c3798aecc871b",
                // index with 17 bytes
                "0000000000000000000000000000000101",
                // child secret key for 17 bytes
                "120fb53090d6cfd1528c83e83af582f96dd105b43f6622df6d797b174429c0f4",
                // child public key for 17 bytes
                "8c6a3c63379c0c48e652ad3190205ec39e6d0679cf47abca5b92915319ecb5f1eda560801e0490aa6f6566b55e132744",
                // large index greater than q, ie Fr::MAX
                "fedcbafedcbafedcbafedcbafedcbafedcbafedcbafedcbafedcbafedcbafedc",
                // child secret key at large index
                "2ffa71ee5cf75392ffcde2ce8d68fb4524453f55ba2e148d0d4a4000da876be6",
                // child public key at large index
                "b492577c7a7e324dec2e34397689e41fa8a894890db931fe93cdb29c5342e1e50ea53c969fae1780677ab27c4ff62fca",
                // index with more than 256 bits
                // note different to single byte index "00"
                "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
                // child secret key for index more than 256 bits
                "10ca7b3cb66ce637d1de47d25cb6817c4b16efcb2221fc60f0190231b2ad656f",
                // child public key for index more than 256 bits
                "8b1d9fada310a22ec2523e42fa1ece8e6bf5b6bc91e591d352dbe96271a9ba9dbecd9a4529befffaf8e57bf929aa227c",
                // index with child secret key leading and trailing zeros
                "000000000014a06d",
                // child secret key for sk leading zero
                "0000ed12dc692ec6401e3e53be147671e1ab934e346fdc146835443e902d0e00",
                // child public key for sk leading zero
                "8258c937cb778d01ee22857b6a120c948638bbf8073e92517b44cde58c1c3117e76d7ee5b62ac3a4cdcdc2971e434643",
                // index with child public key trailing zero
                "0000000000003f51",
                // child secret key for child pk trailing zero
                "16be290c63b85ad7c4db5a5c446e40cb79f7bdd2095589c7f1dd97fc869cb816",
                // child public key for child pk trailing zero
                "9493e3176f8a0f8e5e0f855b57f3f09246c628ccda707919e806192369c9f9b84a5c16d1c6a907c4bad01c17ab560000",
            ],
        ];
        for vector in vectors {
            // get parent keypair
            let sks_bytes = hex::decode(vector[0])?;
            let sks = SecretKeySet::from_bytes(sks_bytes).expect("invalid secret key set bytes");
            // check secret key
            let sk = sks.secret_key();
            let sk_hex = &format!("{}", HexFmt(&sk.to_bytes()));
            assert_eq!(sk_hex, vector[1]);
            // check secret key shares
            let sk_share_0 = sks.secret_key_share(0);
            let sk_share_0_hex = &format!("{}", HexFmt(&sk_share_0.to_bytes()));
            assert_eq!(sk_share_0_hex, vector[2]);
            let sk_share_1 = sks.secret_key_share(1);
            let sk_share_1_hex = &format!("{}", HexFmt(&sk_share_1.to_bytes()));
            assert_eq!(sk_share_1_hex, vector[3]);
            let sk_share_2 = sks.secret_key_share(2);
            let sk_share_2_hex = &format!("{}", HexFmt(&sk_share_2.to_bytes()));
            assert_eq!(sk_share_2_hex, vector[4]);
        }

        Ok(())
    }

    #[test]
    fn test_ciphertext_vectors() -> Result<()> {
        let vectors = vec![
            // Plain old ciphertext
            vec![
                // secret key
                "09f82926174f2fb52fc3674822497362df34186b4cac60ab531d81ac36144b63",
                // plain text hex
                "0102030405",
                // ciphertext
                "9369436c4f3b930aebeb1458b5478a393c90c51de74ebe0ad53b178f25ea0ab51b8acae9847ca3ec9d85bea816e174ca81a7160b714ed5a2a2b6d473473e02345bdeabddad35f13127259b905a8b01ea8225a9449ead9922d8d388959d712bc719889f12f8f273c530e1a7b38a0c2bda9a568453e011c41bb3c66e6dc6c313451802bade49a97e2315507e9a68f1f8794cda1b5420",
            ],
            // Leading zeros and trailing
            vec![
                // secret key
                "0055555555555555555555555555555555555555555555555555555555555500",
                // plain text hex
                "00bdc600",
                // ciphertext with u and w having trailing zeros
                "8d86c6a960cf15f0170b855f5b8d7eca52885fa63ba9c242e54f9cdd5a91f0e42c5b16d39108457613eff00e50b21357af578a279b048d4334434402c129c7754b6461bf653bf57b4b09eb06f53b9360b52438cb9c32c580d9b58981dbf1671519f413245fc288f973d7a47ceca5a21d3e69de7561f70c1c4296f40cdcc0043f20b13e6953fbb1b3363af011350e315fed74a849",
            ],
        ];
        for vector in vectors {
            // get secret key
            let sk_vec =
                hex::decode(vector[0]).map_err(|err| eyre!("invalid msg hex bytes: {}", err))?;
            let mut sk_bytes = [0u8; SK_SIZE];
            sk_bytes[..SK_SIZE].clone_from_slice(&sk_vec[..SK_SIZE]);
            let sk = SecretKey::from_bytes(sk_bytes)
                .map_err(|err| eyre!("invalid secret key bytes: {}", err))?;
            // get ciphertext
            let ct_vec =
                hex::decode(vector[2]).map_err(|err| eyre!("invalid msg hex bytes: {}", err))?;
            let ct = Ciphertext::from_bytes(&ct_vec)
                .map_err(|err| eyre!("invalid ciphertext bytes: {}", err))?;
            // check the ciphertext is valid
            assert!(ct.verify());
            // check the decrypted ciphertext matches the original message
            let msg_vec =
                hex::decode(vector[1]).map_err(|err| eyre!("invalid msg hex bytes: {}", err))?;
            let plaintext = sk.decrypt(&ct).ok_or_else(|| eyre!("decryption failed"))?;
            assert_eq!(plaintext, msg_vec);
        }

        Ok(())
    }

    #[test]
    fn test_sk_set_derive_child() {
        let sks = SecretKeySet::random(3, &mut rand::thread_rng());
        // Deriving from master is the same as deriving a set
        // and getting the master from the derived set
        let mut index = [0u8; 32];
        rand::thread_rng().fill_bytes(&mut index);
        let msk = sks.secret_key();
        let msk_child = msk.derive_child(&index);
        assert_ne!(msk, msk_child);
        let sks_child = sks.derive_child(&index);
        assert_ne!(sks.to_bytes(), sks_child.to_bytes());
        let sks_child_master = sks_child.secret_key();
        assert_eq!(msk_child, sks_child_master);
        // secret key shares are matching
        // sks.child(x).share(y) == sks.share(y).child(x)
        let sks_share0 = sks.secret_key_share(0);
        let sks_share0_child = sks_share0.derive_child(&index);
        let sks_child_share0 = sks_child.secret_key_share(0);
        assert_eq!(sks_share0_child, sks_child_share0);
    }

    #[test]
    fn test_pk_set_derive_child() {
        let sks = SecretKeySet::random(3, &mut rand::thread_rng());
        let pks = sks.public_keys();
        // Deriving from master is the same as deriving a set
        // and getting the master from the derived set
        let mut index = [0u8; 32];
        rand::thread_rng().fill_bytes(&mut index);
        let mpk = pks.public_key();
        let mpk_child = mpk.derive_child(&index);
        assert_ne!(mpk, mpk_child);
        let pks_child = pks.derive_child(&index);
        assert_ne!(pks.to_bytes(), pks_child.to_bytes());
        let pks_child_master = pks_child.public_key();
        assert_eq!(mpk_child, pks_child_master);
        // public key shares are matching
        // pks.child(x).share(y) == pks.share(y).child(x)
        let pks_share0 = pks.public_key_share(0);
        let pks_share0_child = pks_share0.derive_child(&index);
        let pks_child_share0 = pks_child.public_key_share(0);
        assert_eq!(pks_share0_child, pks_child_share0);
        // derived master public key is a pair for derived master secret key
        let sks_child = sks.derive_child(&index);
        assert_eq!(sks_child.secret_key().public_key(), pks_child.public_key());
    }

    #[test]
    fn test_sk_set_child_sig() -> Result<()> {
        // combining signatures from child keyshares produces
        // a valid signature for the child public key set
        let mut rng = rand::thread_rng();
        // The threshold is 3, so 4 signature shares will suffice to decrypt.
        let sks = SecretKeySet::random(3, &mut rng);
        let share_indexes = vec![5, 8, 7, 10];
        // all participants have the public key set and their key share.
        let pks = sks.public_keys();
        let key_shares: BTreeMap<_, _> = share_indexes
            .iter()
            .map(|&i| {
                let key_share = sks.secret_key_share(i);
                (i, key_share)
            })
            .collect();
        // all participants use the same index to derive a child keyshare
        let mut index = [0u8; 32];
        rng.fill_bytes(&mut index);
        let child_key_shares: BTreeMap<_, _> = key_shares
            .iter()
            .map(|(i, key_share)| {
                let child_key_share = key_share.derive_child(&index);
                (i, child_key_share)
            })
            .collect();
        // all participants sign a message with their child keyshare
        let msg = "Totally real news";
        let mut child_sig_shares = BTreeMap::default();
        for (i, child_key_share) in child_key_shares.iter() {
            let child_sig_share = child_key_share.sign(msg);
            child_sig_shares.insert(i, child_sig_share);
        }
        // Combining the child shares creates a valid signature for the child
        // public key set.
        let pks_child = pks.derive_child(&index);
        let sig = pks_child
            .combine_signatures(&child_sig_shares)
            .map_err(|err| eyre!("signatures match: {}", err))?;
        assert!(pks_child.public_key().verify(&sig, msg));

        Ok(())
    }

    #[test]
    fn test_zero_pubkey_attack() {
        let sk = SecretKey::random();
        let pk = sk.public_key();

        // Make sure the public key is not zero
        assert!(!pk.is_zero());

        // Rogue 0 pubkey
        let rogue_public_key = PublicKey(G1Affine::identity());
        assert!(rogue_public_key.is_zero());

        // Rogue 0 sig
        let rogue_sig = Signature(G2Affine::identity());

        // just any hash will do
        let hash = hash_g2(b"anything");

        // check that the attack works without the 0 check
        assert_eq!(
            PEngine::pairing(&rogue_public_key.0, &hash),
            PEngine::pairing(&G1Affine::generator(), &rogue_sig.0)
        );

        // check that verify_g2 is protected against this attack
        assert!(!rogue_public_key.verify_g2(&rogue_sig, hash));
    }
}
