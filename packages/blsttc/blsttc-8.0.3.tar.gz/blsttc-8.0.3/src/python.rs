use pyo3::prelude::*;
use crate::{SecretKey, PublicKey, Signature, SecretKeySet, PublicKeySet, DecryptionShare, Ciphertext};
use crate::error::Error;
use rand::thread_rng;
use std::collections::BTreeMap;

impl From<Error> for PyErr {
    fn from(err: Error) -> PyErr {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
    }
}

#[pyclass]
pub struct PySecretKey(SecretKey);

#[pyclass]
pub struct PyPublicKey(PublicKey);

#[pyclass]
pub struct PySignature(Signature);

#[pyclass]
pub struct PySecretKeySet(SecretKeySet);

#[pyclass]
pub struct PyPublicKeySet(PublicKeySet);

#[pyclass]
#[derive(Clone)]
pub struct PyDecryptionShare(DecryptionShare);

#[pymethods]
impl PySecretKey {
    #[new]
    pub fn new() -> Self {
        PySecretKey(SecretKey::random())
    }

    pub fn sign(&self, msg: &[u8]) -> PyResult<PySignature> {
        Ok(PySignature(self.0.sign(msg)))
    }

    pub fn public_key(&self) -> PyPublicKey {
        PyPublicKey(self.0.public_key())
    }

    pub fn to_bytes(&self) -> PyResult<Vec<u8>> {
        Ok(self.0.to_bytes().to_vec())
    }

    #[staticmethod]
    pub fn from_bytes(bytes: &[u8]) -> PyResult<Self> {
        let array: [u8; 32] = bytes.try_into()
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid byte length"))?;
        Ok(PySecretKey(SecretKey::from_bytes(array)?))
    }

    pub fn derive_child(&self, index: &[u8]) -> PyResult<Self> {
        Ok(PySecretKey(self.0.derive_child(index)))
    }
}

#[pymethods]
impl PyPublicKey {
    pub fn verify(&self, signature: &PySignature, msg: &[u8]) -> bool {
        self.0.verify(&signature.0, msg)
    }

    pub fn encrypt(&self, msg: &[u8]) -> PyResult<Vec<u8>> {
        Ok(self.0.encrypt(msg).to_bytes().to_vec())
    }

    pub fn to_bytes(&self) -> PyResult<Vec<u8>> {
        Ok(self.0.to_bytes().to_vec())
    }

    #[staticmethod]
    pub fn from_bytes(bytes: &[u8]) -> PyResult<Self> {
        let array: [u8; 48] = bytes.try_into()
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid byte length"))?;
        Ok(PyPublicKey(PublicKey::from_bytes(array)?))
    }
}

#[pymethods]
impl PySecretKeySet {
    #[new]
    pub fn new(threshold: usize) -> PyResult<Self> {
        Ok(PySecretKeySet(SecretKeySet::random(threshold, &mut thread_rng())))
    }

    pub fn threshold(&self) -> usize {
        self.0.threshold()
    }

    pub fn secret_key_share(&self, index: usize) -> PyResult<PySecretKey> {
        Ok(PySecretKey(self.0.secret_key_share(index).0))
    }

    pub fn public_keys(&self) -> PyPublicKeySet {
        PyPublicKeySet(self.0.public_keys())
    }

    pub fn decrypt_share(&self, index: usize, ciphertext: &[u8]) -> PyResult<PyDecryptionShare> {
        let ct = Ciphertext::from_bytes(ciphertext)
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid ciphertext"))?;
        Ok(PyDecryptionShare(self.0.secret_key_share(index).decrypt_share(&ct)
            .ok_or_else(|| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid ciphertext"))?))
    }
}

#[pymethods]
impl PyPublicKeySet {
    pub fn threshold(&self) -> usize {
        self.0.threshold()
    }

    pub fn public_key(&self) -> PyPublicKey {
        PyPublicKey(self.0.public_key())
    }

    pub fn public_key_share(&self, index: usize) -> PyResult<PyPublicKey> {
        Ok(PyPublicKey(self.0.public_key_share(index).0))
    }

    pub fn decrypt(&self, shares: Vec<(usize, PyDecryptionShare)>, ciphertext: &[u8]) -> PyResult<Vec<u8>> {
        let ct = Ciphertext::from_bytes(ciphertext)
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid ciphertext"))?;
        
        let shares_map: BTreeMap<_, _> = shares.into_iter()
            .map(|(i, share)| (i, share.0))
            .collect();
        
        Ok(self.0.decrypt(&shares_map, &ct)?.to_vec())
    }
}

#[pymethods]
impl PyDecryptionShare {
    pub fn to_bytes(&self) -> PyResult<Vec<u8>> {
        Ok(self.0.to_bytes().to_vec())
    }

    #[staticmethod]
    pub fn from_bytes(bytes: &[u8]) -> PyResult<Self> {
        let array: [u8; 48] = bytes.try_into()
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyValueError, _>("Invalid byte length"))?;
        Ok(PyDecryptionShare(DecryptionShare::from_bytes(array)?))
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn _blsttc(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<PySecretKey>()?;
    m.add_class::<PyPublicKey>()?;
    m.add_class::<PySignature>()?;
    m.add_class::<PySecretKeySet>()?;
    m.add_class::<PyPublicKeySet>()?;
    m.add_class::<PyDecryptionShare>()?;
    Ok(())
}
