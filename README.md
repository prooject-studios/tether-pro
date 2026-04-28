# Tether Pro

Tether Pro is a desktop password manager (Python UI + Rust crypto core).

![Security](https://img.shields.io/badge/Security-High-red?style=for-the-badge)
![Language](https://img.shields.io/badge/Rust-Core-orange?style=for-the-badge)
![Language](https://img.shields.io/badge/Python-UI-blue?style=for-the-badge)

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

## 🤝 Contributing

I welcome any help with the development of Tether Pro! If you want to suggest changes or fix a bug, please follow these steps:

1. **Clone the repository** (via terminal or GitHub Desktop).
2. **Create a new branch** for your changes.
   - *Important:* Use the naming format `username_branch` (e.g., `smith_fix-encryption`). This makes it much easier for me to manage the project and identify the author of the changes.
3. **Make your changes** and commit them.
4. **Publish your branch** and create a **Pull Request** to the main branch.

> [!IMPORTANT]
> Pull Requests from branches named according to the `username_branch` standard will be prioritized for code review and merging!