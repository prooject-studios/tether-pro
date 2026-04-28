use pyo3::prelude::*;
use std::fs;
use std::path::Path;
use sysinfo::{DiskExt, System, SystemExt};

#[pyfunction]
fn check_hardware_key(target_file: String) -> PyResult<bool> {
    let mut sys = System::new_all();
    sys.refresh_disks();

    for disk in sys.disks() {
        let mount_point = disk.mount_point();
        // Пытаемся найти файл-соль на каждом подключенном диске
        let potential_path = mount_point.join(&target_file);
        
        if potential_path.exists() {
            return Ok(true);
        }
    }
    Ok(false)
}

#[pyfunction]
fn generate_salt() -> PyResult<String> {
    // В будущем тут будет генерация криптографической соли
    Ok("generated_salt_example".to_string())
}

#[pymodule]
fn tether_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(check_hardware_key, m)?)?;
    m.add_function(wrap_pyfunction!(generate_salt, m)?)?;
    Ok(())
}