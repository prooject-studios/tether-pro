import customtkinter as ctk
from tkinter import messagebox

# Премиальная синяя палитра (Tech-Dark)
COLORS = {
    "bg": "#0D1117",         # Глубокий темный сине-серый (как в GitHub Dark)
    "sidebar": "#161B22",    # Чуть светлее для бокового меню
    "card": "#21262D",       # Цвет карточек и полей
    "accent": "#58A6FF",     # Яркий акцентный синий для кнопок и индикаторов
    "text": "#F0F6FC",       # Основной белый
    "muted": "#8B949E",      # Тусклый текст
    "danger": "#F85149"      # Красный для ошибок/блокировки
}

class TetherPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TETHER PRO — Vault Interface")
        self.geometry("1100x650")
        self.configure(fg_color=COLORS["bg"])

        # Настройка сетки приложения
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.is_locked = True
        self.setup_sidebar()
        self.setup_main_view()

    def setup_sidebar(self):
        """Профессиональное боковое меню"""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=COLORS["sidebar"], border_width=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)

        # Логотип
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🛡️ TETHER PRO", font=("Segoe UI", 20, "bold"), text_color=COLORS["accent"])
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 40))

        # Навигационные кнопки
        self.btn_vault = self.create_nav_btn("🔐 Хранилище", 1)
        self.btn_gen = self.create_nav_btn("🔑 Генератор", 2)
        self.btn_settings = self.create_nav_btn("⚙️ Настройки", 3)

        # Нижний статус-бар безопасности
        self.status_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.status_frame.grid(row=5, column=0, pady=25, padx=20, sticky="s")
        
        self.hw_indicator = ctk.CTkLabel(
            self.status_frame, 
            text="● Ключ USB: Отсутствует", 
            text_color=COLORS["danger"], 
            font=("Segoe UI", 12, "bold")
        )
        self.hw_indicator.pack()

    def create_nav_btn(self, text, row):
        """Создание стильной кнопки меню"""
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            corner_radius=6, 
            height=42,
            fg_color="transparent", 
            hover_color=COLORS["card"],
            text_color=COLORS["text"],
            anchor="w", 
            font=("Segoe UI", 13)
        )
        btn.grid(row=row, column=0, padx=15, pady=6, sticky="ew")
        return btn

    def setup_main_view(self):
        """Зона основного контента"""
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=40, pady=35)
        
        if self.is_locked:
            self.show_auth_screen()

    def show_auth_screen(self):
        """Экран ввода мастер-ключа"""
        self.auth_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.auth_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.auth_frame, 
            text="ТРЕБУЕТСЯ АВТОРИЗАЦИЯ", 
            font=("Segoe UI", 14, "bold"), 
            text_color=COLORS["muted"]
        ).pack(pady=10)

        self.master_pwd = ctk.CTkEntry(
            self.auth_frame, 
            placeholder_text="Введите мастер-пароль",
            width=380, 
            height=45, 
            show="*", 
            border_width=1,
            fg_color=COLORS["card"], 
            border_color="#30363D",
            text_color=COLORS["text"]
        )
        self.master_pwd.pack(pady=10)

        self.unlock_btn = ctk.CTkButton(
            self.auth_frame, 
            text="Расшифровать данные", 
            fg_color=COLORS["accent"], 
            hover_color="#388BFD",
            text_color="#0D1117", # Контрастный темный текст на синем фоне
            font=("Segoe UI", 13, "bold"),
            width=380, 
            height=45, 
            command=self.attempt_unlock
        )
        self.unlock_btn.pack(pady=15)

    def attempt_unlock(self):
        """Процесс разблокировки"""
        # Позже здесь будет Rust-функция
        self.hw_indicator.configure(text="● Ключ USB: Активен", text_color="#3FB950") # Зеленый
        self.auth_frame.destroy()
        self.show_vault_dashboard()

    def show_vault_dashboard(self):
        """Панель управления паролями"""
        header = ctk.CTkLabel(
            self.main_container, 
            text="Мои пароли", 
            font=("Segoe UI", 24, "bold"), 
            text_color=COLORS["text"]
        )
        header.pack(anchor="w", pady=(0, 25))

        # Поиск
        search_bar = ctk.CTkEntry(
            self.main_container, 
            placeholder_text="Поиск по сервисам...", 
            height=40, 
            fg_color=COLORS["card"], 
            border_color="#30363D",
            border_width=1,
            text_color=COLORS["text"]
        )
        search_bar.pack(fill="x", pady=(0, 15))

        # Скролл-контейнер для паролей
        self.scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True)

        # Тестовое наполнение
        self.add_password_card("GitHub", "dev_acc@email.com")
        self.add_password_card("ProtonMail", "secure_box@pm.me")
        self.add_password_card("Crypto Wallet", "wallet_main")

    def add_password_card(self, service, login):
        """Создание карточки пароля"""
        card = ctk.CTkFrame(self.scroll, fg_color=COLORS["card"], height=70, border_color="#30363D", border_width=1)
        card.pack(fill="x", pady=6)
        
        # Левая часть с информацией
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=20, fill="y")
        
        ctk.CTkLabel(info_frame, text=service, font=("Segoe UI", 14, "bold"), text_color=COLORS["text"]).pack(anchor="w", pady=(10, 0))
        ctk.CTkLabel(info_frame, text=login, font=("Segoe UI", 12), text_color=COLORS["muted"]).pack(anchor="w")
        
        # Правая часть с кнопками управления
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(side="right", padx=15, fill="y")
        
        ctk.CTkButton(btn_frame, text="Копировать", width=90, height=30, 
                     fg_color="#30363D", hover_color="#484F58", text_color=COLORS["text"]).pack(side="left", padx=5, pady=20)
        ctk.CTkButton(btn_frame, text="Изменить", width=90, height=30,
                     fg_color="#30363D", hover_color="#484F58", text_color=COLORS["text"]).pack(side="left", padx=5, pady=20)

if __name__ == "__main__":
    app = TetherPro()
    app.mainloop()