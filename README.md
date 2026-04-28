# Tether Pro

Tether Pro is a desktop password manager (Python UI + Rust crypto core).

## Quick start (Windows, from fresh GitHub clone)

1. Clone repository:
```powershell
git clone https://github.com/<your-username>/tether-pro.git
cd tether-pro/TetherPro
```

2. Run one-time setup:
```powershell
.\setup.ps1
```

3. Start app:
```powershell
.\run.ps1
```

After this, users can run only `./run.ps1`.

## What setup.ps1 does

- creates `.venv`
- installs Python dependencies
- builds and installs Rust extension `tether_core` with `maturin develop --release`

## Requirements

- Python 3.10+
- Rust toolchain (`rustup`, `cargo`)
- Windows PowerShell

## Project layout

- `TetherPro/main.py` - app entry point
- `TetherPro/ui/` - CustomTkinter UI
- `TetherPro/data/manager.py` - vault/storage logic
- `TetherPro/core/` - Rust crypto module (PyO3)
