use aes_gcm::aead::{Aead, KeyInit};
use aes_gcm::{Aes256Gcm, Nonce};
use argon2::Argon2;
use base64::{engine::general_purpose, Engine as _};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use rand::RngCore;
use sha2::{Digest, Sha256};
use sysinfo::Disks;

fn derive_key(password: &str, salt_hex: &str) -> PyResult<[u8; 32]> {
    let salt = hex_to_bytes(salt_hex)?;
    let mut key = [0u8; 32];

    Argon2::default()
        .hash_password_into(password.as_bytes(), &salt, &mut key)
        .map_err(|e| PyValueError::new_err(format!("failed to derive key: {e}")))?;

    Ok(key)
}

fn hex_to_bytes(value: &str) -> PyResult<Vec<u8>> {
    if value.len() % 2 != 0 {
        return Err(PyValueError::new_err("salt hex length must be even"));
    }

    let mut result = Vec::with_capacity(value.len() / 2);
    for i in (0..value.len()).step_by(2) {
        let part = &value[i..i + 2];
        let byte = u8::from_str_radix(part, 16)
            .map_err(|_| PyValueError::new_err("invalid salt hex format"))?;
        result.push(byte);
    }
    Ok(result)
}

#[pyfunction]
fn check_hardware_key(target_file: String) -> PyResult<bool> {
    let disks = Disks::new_with_refreshed_list();
    for disk in &disks {
        let mount_point = disk.mount_point();
        let potential_path = mount_point.join(&target_file);

        if potential_path.exists() {
            return Ok(true);
        }
    }
    Ok(false)
}

#[pyfunction]
fn generate_salt() -> PyResult<String> {
    let mut random = [0u8; 16];
    rand::thread_rng().fill_bytes(&mut random);

    let mut hasher = Sha256::new();
    hasher.update(random);
    let hashed = hasher.finalize();

    Ok(hex::encode(&hashed[..16]))
}

#[pyfunction]
fn encrypt_payload(payload: String, password: String, salt_hex: String) -> PyResult<String> {
    let key = derive_key(&password, &salt_hex)?;
    let cipher = Aes256Gcm::new_from_slice(&key)
        .map_err(|_| PyValueError::new_err("invalid key length"))?;

    let mut nonce_bytes = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut nonce_bytes);
    let nonce = Nonce::from_slice(&nonce_bytes);

    let encrypted = cipher
        .encrypt(nonce, payload.as_bytes())
        .map_err(|_| PyValueError::new_err("encryption failed"))?;

    let nonce_b64 = general_purpose::STANDARD.encode(nonce_bytes);
    let data_b64 = general_purpose::STANDARD.encode(encrypted);
    Ok(format!("{nonce_b64}:{data_b64}"))
}

#[pyfunction]
fn decrypt_payload(payload: String, password: String, salt_hex: String) -> PyResult<String> {
    let mut split = payload.splitn(2, ':');
    let nonce_part = split
        .next()
        .ok_or_else(|| PyValueError::new_err("invalid encrypted payload format"))?;
    let data_part = split
        .next()
        .ok_or_else(|| PyValueError::new_err("invalid encrypted payload format"))?;

    let nonce_vec = general_purpose::STANDARD
        .decode(nonce_part)
        .map_err(|_| PyValueError::new_err("invalid nonce encoding"))?;
    if nonce_vec.len() != 12 {
        return Err(PyValueError::new_err("invalid nonce length"));
    }

    let data = general_purpose::STANDARD
        .decode(data_part)
        .map_err(|_| PyValueError::new_err("invalid data encoding"))?;

    let key = derive_key(&password, &salt_hex)?;
    let cipher = Aes256Gcm::new_from_slice(&key)
        .map_err(|_| PyValueError::new_err("invalid key length"))?;

    let nonce = Nonce::from_slice(&nonce_vec);
    let decrypted = cipher
        .decrypt(nonce, data.as_ref())
        .map_err(|_| PyValueError::new_err("decryption failed"))?;

    String::from_utf8(decrypted).map_err(|_| PyValueError::new_err("decrypted data is not utf-8"))
}

#[pymodule]
fn tether_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(check_hardware_key, m)?)?;
    m.add_function(wrap_pyfunction!(generate_salt, m)?)?;
    m.add_function(wrap_pyfunction!(encrypt_payload, m)?)?;
    m.add_function(wrap_pyfunction!(decrypt_payload, m)?)?;
    Ok(())
}
