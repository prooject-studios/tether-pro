import customtkinter as ctk
from tkinter import messagebox
import sys

# Попытка импорта Rust-ядра
try:
    import tether_core
except ImportError:
    # Заглушка на случай, если ядро еще не скомпилировано через maturin
    tether_core = None

# Премиальная синяя палитра (GitHub Dark Style)
COLORS = {
    "bg": "#0D1117",
    "sidebar": "#161B22",
    "card": "#21262D",
    "accent": "#58A6FF",
    "text": "#F0F6FC",
    "muted": "#8B949E",
    "danger": "#F85149",
    "success": "#3FB950"
}

class TetherPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TETHER PRO — Hardware-Bound Vault")
        self.geometry("1100x650")
        self.configure(fg_color=COLORS["bg"])

        # Сетка приложения
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.is_locked = True
        self.current_frame = None

        self.setup_sidebar()
        self.setup_main_container()
        
        # По умолчанию показываем экран авторизации
        self.show_auth_screen()

    def setup_sidebar(self):
        """Боковое меню навигации"""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLORS["sidebar"], border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        # Лого
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="🛡️ TETHER PRO", 
            font=("Segoe UI", 20, "bold"), 
            text_color=COLORS["accent"]
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 40))

        # Навигация
        self.nav_vault = self.create_nav_btn("🔐 Хранилище", 1, lambda: self.show_vault_dashboard())
        self.nav_gen = self.create_nav_btn("🔑 Генератор", 2, lambda: self.show_placeholder("Генератор паролей"))
        self.nav_settings = self.create_nav_btn("⚙️ Настройки", 3, lambda: self.show_placeholder("Настройки системы"))

        # Индикатор USB
        self.status_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.status_frame.grid(row=5, column=0, pady=25, padx=20, sticky="s")
        
        self.hw_indicator = ctk.CTkLabel(
            self.status_frame, 
            text="● HW_KEY: DISCONNECTED", 
            text_color=COLORS["danger"], 
            font=("Consolas", 11, "bold")
        )
        self.hw_indicator.pack()

    def create_nav_btn(self, text, row, command):
        btn = ctk.CTkButton(
            self.sidebar, text=text, corner_radius=6, height=42,
            fg_color="transparent", hover_color=COLORS["card"],
            text_color=COLORS["text"], anchor="w", font=("Segoe UI", 13),
            command=command
        )
        btn.grid(row=row, column=0, padx=15, pady=6, sticky="ew")
        return btn

    def setup_main_container(self):
        """Контейнер, в котором будут меняться экраны"""
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=40, pady=35)

    def clear_main_container(self):
        """Очистка текущего экрана"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_auth_screen(self):
        """Экран входа"""
        self.clear_main_container()
        
        auth_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        auth_view.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            auth_view, text="ТРЕБУЕТСЯ КЛЮЧ ДЕШИФРОВАНИЯ", 
            font=("Segoe UI", 13, "bold"), text_color=COLORS["muted"]
        ).pack(pady=10)

        self.master_pwd = ctk.CTkEntry(
            auth_view, placeholder_text="Введите мастер-пароль",
            width=380, height=48, show="*", border_width=1,
            fg_color=COLORS["card"], border_color="#30363D"
        )
        self.master_pwd.pack(pady=10)

        self.unlock_btn = ctk.CTkButton(
            auth_view, text="РАСШИФРОВАТЬ", 
            fg_color=COLORS["accent"], hover_color="#388BFD",
            text_color="#0D1117", font=("Segoe UI", 13, "bold"),
            width=380, height=48, command=self.attempt_unlock
        )
        self.unlock_btn.pack(pady=15)

    def attempt_unlock(self):
        """Логика разблокировки через Rust-ядро"""
        if tether_core is None:
            messagebox.showwarning("System", "Ядро tether_core не найдено. Работа в демо-режиме.")
            self.unlock_success()
            return

        # Вызов функции из Rust
        # Ищем файл 'salt.tether' на всех USB дисках
        if tether_core.check_hardware_key("salt.tether"):
            self.unlock_success()
        else:
            self.hw_indicator.configure(text="● HW_KEY: NOT FOUND", text_color=COLORS["danger"])
            messagebox.showerror("Security Alert", "Физический ключ (USB) не обнаружен.\nВставьте флешку с файлом 'salt.tether'")

    def unlock_success(self):
        self.is_locked = False
        self.hw_indicator.configure(text="● HW_KEY: ACTIVE", text_color=COLORS["success"])
        self.show_vault_dashboard()

    def show_vault_dashboard(self):
        if self.is_locked:
            self.show_auth_screen()
            return

        self.clear_main_container()
        
        header = ctk.CTkLabel(self.main_container, text="Менеджер паролей", font=("Segoe UI", 24, "bold"))
        header.pack(anchor="w", pady=(0, 20))

        search_bar = ctk.CTkEntry(
            self.main_container, placeholder_text="Поиск записей...", 
            height=40, fg_color=COLORS["card"], border_color="#30363D"
        )
        search_bar.pack(fill="x", pady=(0, 20))

        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent", label_text="Защищенные записи")
        scroll.pack(fill="both", expand=True)

        # Пример данных
        data = [("GitHub", "login_user"), ("Binance", "crypto_holder"), ("Work Mail", "dev@firm.com")]
        for service, user in data:
            self.add_card(scroll, service, user)

    def add_card(self, parent, service, user):
        card = ctk.CTkFrame(parent, fg_color=COLORS["card"], height=70, border_color="#30363D", border_width=1)
        card.pack(fill="x", pady=6)
        
        lbl_frame = ctk.CTkFrame(card, fg_color="transparent")
        lbl_frame.pack(side="left", padx=20, fill="y")
        
        ctk.CTkLabel(lbl_frame, text=service, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(lbl_frame, text=user, font=("Segoe UI", 12), text_color=COLORS["muted"]).pack(anchor="w")
        
        # Кнопки
        btn_view = ctk.CTkButton(card, text="👀", width=40, fg_color="#30363D", hover_color="#484F58")
        btn_view.pack(side="right", padx=10, pady=15)
        
        btn_copy = ctk.CTkButton(card, text="Копировать", width=100, fg_color="#30363D", hover_color="#484F58")
        btn_copy.pack(side="right", padx=5, pady=15)

    def show_placeholder(self, title):
        """Временный экран для разделов в разработке"""
        if self.is_locked: return
        self.clear_main_container()
        ctk.CTkLabel(self.main_container, text=title, font=("Segoe UI", 24, "bold")).pack(pady=100)
        ctk.CTkLabel(self.main_container, text="Раздел находится в разработке...", text_color=COLORS["muted"]).pack()

if __name__ == "__main__":
    app = TetherPro()
    app.mainloop()