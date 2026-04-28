import customtkinter as ctk
from ui.components import COLORS, AnimatedButton, VaultCard

class TetherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TETHER PRO — Workstation")
        self.geometry("1100x650")
        self.configure(fg_color=COLORS["bg"])

        # Сетка
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.show_dashboard()

    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=260, fg_color=COLORS["sidebar"], corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(sidebar, text="🛡️ TETHER PRO", font=("Segoe UI", 20, "bold")).pack(pady=40)
        
        # Кнопки разделов
        self.add_nav_btn(sidebar, "🔐 Сейфы", self.show_dashboard)
        self.add_nav_btn(sidebar, "⚙️ Настройки", self.show_settings)

    def add_nav_btn(self, master, text, command):
        btn = ctk.CTkButton(master, text=text, fg_color="transparent", anchor="w", 
                            hover_color=COLORS["card"], command=command)
        btn.pack(fill="x", padx=15, pady=5)

    def show_dashboard(self):
        self.clear_main()
        header = ctk.CTkLabel(self.main_container, text="Ваши пароли", font=("Segoe UI", 24, "bold"))
        header.pack(anchor="w", pady=(0, 20))
        
        # Пример использования компонента из components.py
        VaultCard(self.main_container, "GitHub", "Loocik").pack(fill="x", pady=5)
        VaultCard(self.main_container, "Google", "alex.r@tech.ru").pack(fill="x", pady=5)

    def show_settings(self):
        self.clear_main()
        ctk.CTkLabel(self.main_container, text="Настройки", font=("Segoe UI", 24, "bold")).pack(anchor="w")
        ctk.CTkSwitch(self.main_container, text="HWID Привязка").pack(pady=20, anchor="w")

    def clear_main(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()