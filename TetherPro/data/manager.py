import json
import hashlib
import hmac
import secrets
from pathlib import Path

try:
    import tether_core as core
except ImportError:
    core = None


class DataManager:
    DB_PATH = Path("vault.tether")
    _session_password = None

    @staticmethod
    def _read_payload():
        if not DataManager.DB_PATH.exists():
            return None

        with DataManager.DB_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _write_payload(payload):
        with DataManager.DB_PATH.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _derive_hash(password: str, salt_hex: str) -> str:
        salt = bytes.fromhex(salt_hex)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
        return digest.hex()

    @staticmethod
    def _require_session_password() -> str:
        if not DataManager._session_password:
            raise RuntimeError("Session is locked. Please login again.")
        return DataManager._session_password

    @staticmethod
    def _require_core():
        if core is None:
            raise RuntimeError("tether_core is not available. Build the Rust module first.")

    @staticmethod
    def is_first_launch():
        return not DataManager.DB_PATH.exists()

    @staticmethod
    def setup_master(password):
        DataManager._require_core()
        salt_hex = secrets.token_bytes(16).hex()
        empty_entries = json.dumps([], ensure_ascii=False)
        encrypted_entries = core.encrypt_payload(empty_entries, password, salt_hex)

        payload = {
            "version": 2,
            "salt": salt_hex,
            "master_hash": DataManager._derive_hash(password, salt_hex),
            "entries_enc": encrypted_entries,
        }
        DataManager._write_payload(payload)
        DataManager._session_password = password

    @staticmethod
    def verify_master(password):
        payload = DataManager._read_payload()
        if not payload:
            return False

        expected = payload.get("master_hash", "")
        salt_hex = payload.get("salt", "")
        actual = DataManager._derive_hash(password, salt_hex)
        is_valid = hmac.compare_digest(expected, actual)

        if is_valid:
            DataManager._session_password = password

        return is_valid

    @staticmethod
    def load_entries():
        DataManager._require_core()
        payload = DataManager._read_payload() or {}

        # Migration from old plaintext schema.
        if "entries" in payload and "entries_enc" not in payload:
            entries = payload.get("entries", [])
            DataManager.save_entries(entries)
            return entries

        encrypted = payload.get("entries_enc")
        if not encrypted:
            return []

        password = DataManager._require_session_password()
        decrypted = core.decrypt_payload(encrypted, password, payload.get("salt", ""))
        return json.loads(decrypted)

    @staticmethod
    def save_entries(entries):
        DataManager._require_core()
        payload = DataManager._read_payload() or {}
        password = DataManager._require_session_password()

        raw = json.dumps(entries, ensure_ascii=False)
        payload["entries_enc"] = core.encrypt_payload(raw, password, payload.get("salt", ""))
        payload.pop("entries", None)
        payload["version"] = 2

        DataManager._write_payload(payload)

    @staticmethod
    def check_hardware_key(target_file="tether.key"):
        try:
            return bool(core.check_hardware_key(target_file))
        except Exception:
            return False
