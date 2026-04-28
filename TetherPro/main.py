import customtkinter as ctk
from ui.app import TetherApp
from ui.auth import AuthWindow
from data.manager import DataManager

def main():
    ctk.set_appearance_mode("dark")
    
    if DataManager.is_first_launch():
        # Показываем окно регистрации мастер-пароля
        app = AuthWindow(mode="register")
    else:
        # Показываем обычный вход
        app = AuthWindow(mode="login")
    
    app.mainloop()

    # Если авторизация успешна, AuthWindow закроется и откроет TetherApp
    # (Это реализуется через callback-функции)

if __name__ == "__main__":
    main()