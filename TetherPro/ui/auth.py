import customtkinter as ctk
from data.manager import DataManager
from ui.app import TetherApp


class AuthWindow(ctk.CTk):
    def __init__(self, mode="login"):
        super().__init__()
        self.mode = mode
        self._status_var = ctk.StringVar(value="")
        self.setup_ui()

    def setup_ui(self):
        self.geometry("460x420")
        self.minsize(460, 420)
        self.configure(fg_color="#0B1220")

        if self.mode == "register":
            self.title("Tether Pro: Первый запуск")
            self.render_registration()
        else:
            self.title("Tether Pro: Вход")
            self.render_login()

    def _base_form(self, title_text, subtitle_text):
        card = ctk.CTkFrame(self, fg_color="#121C2F", corner_radius=16)
        card.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(
            card,
            text=title_text,
            font=("Segoe UI", 24, "bold"),
            text_color="#E7EDF9"
        ).pack(pady=(24, 8))

        ctk.CTkLabel(
            card,
            text=subtitle_text,
            font=("Segoe UI", 13),
            text_color="#9CB0D0"
        ).pack(pady=(0, 20))

        status = ctk.CTkLabel(
            card,
            textvariable=self._status_var,
            font=("Segoe UI", 12),
            text_color="#FF7B7B"
        )
        status.pack(pady=(4, 6))
        return card

    def render_registration(self):
        card = self._base_form(
            "Создать мастер-пароль",
            "Он используется для входа в зашифрованное хранилище"
        )

        self.p1 = ctk.CTkEntry(card, placeholder_text="Мастер-пароль", show="*", width=340, height=42)
        self.p1.pack(pady=8)
        self.p2 = ctk.CTkEntry(card, placeholder_text="Повторите пароль", show="*", width=340, height=42)
        self.p2.pack(pady=8)

        ctk.CTkButton(
            card,
            text="Создать хранилище",
            command=self.create_vault,
            width=340,
            height=42,
            fg_color="#2F7FFF",
            hover_color="#2367D8",
            text_color="#ECF3FF"
        ).pack(pady=(20, 8))

    def render_login(self):
        card = self._base_form(
            "Вход в Tether Pro",
            "Введите мастер-пароль для доступа к хранилищу"
        )

        self.password = ctk.CTkEntry(card, placeholder_text="Мастер-пароль", show="*", width=340, height=42)
        self.password.pack(pady=(8, 10))

        ctk.CTkButton(
            card,
            text="Войти",
            command=self.login,
            width=340,
            height=42,
            fg_color="#2F7FFF",
            hover_color="#2367D8",
            text_color="#ECF3FF"
        ).pack(pady=(10, 8))

    def create_vault(self):
        p1 = self.p1.get().strip()
        p2 = self.p2.get().strip()

        if len(p1) < 8:
            self._status_var.set("Пароль должен быть не короче 8 символов")
            return

        if p1 != p2:
            self._status_var.set("Пароли не совпадают")
            return

        DataManager.setup_master(p1)
        self.open_main_app()

    def login(self):
        password = self.password.get().strip()
        if not password:
            self._status_var.set("Введите пароль")
            return

        if not DataManager.verify_master(password):
            self._status_var.set("Неверный мастер-пароль")
            return

        self.open_main_app()

    def open_main_app(self):
        self.destroy()
        app = TetherApp()
        app.mainloop()
