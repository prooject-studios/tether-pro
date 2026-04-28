import os
import tether_pro as core

class DataManager:
    DB_PATH = "vault.tether"

    @staticmethod
    def is_first_launch():
        # Если файла базы нет, значит пользователь новый
        return not os.path.exists(DataManager.DB_PATH)

    @staticmethod
    def setup_master(password):
        # Вызываем Rust-ядро, чтобы создать зашифрованный заголовок базы
        # core.init_vault(password, DataManager.DB_PATH)
        pass

    @staticmethod
    def save_data(data, password):
        # Шифруем через Rust и сохраняем
        pass