import customtkinter as ctk
from ui.auth import AuthWindow
from data.manager import DataManager


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    mode = "register" if DataManager.is_first_launch() else "login"
    app = AuthWindow(mode=mode)
    app.mainloop()


if __name__ == "__main__":
    main()
