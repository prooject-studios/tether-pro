import customtkinter as ctk
from ui.components import COLORS, AnimatedButton, VaultCard
from data.manager import DataManager


class TetherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tether Pro | Workstation")
        self.geometry("1160x700")
        self.minsize(980, 620)
        self.configure(fg_color=COLORS["bg"])
        self.entries = DataManager.load_entries()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=32, pady=28)

        self.show_dashboard()

    def setup_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=270, fg_color=COLORS["sidebar"], corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            sidebar,
            text="TETHER PRO",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS["text"]
        ).pack(pady=(34, 8), padx=20, anchor="w")

        ctk.CTkLabel(
            sidebar,
            text="Secure workstation",
            font=("Segoe UI", 12),
            text_color=COLORS["muted"]
        ).pack(pady=(0, 24), padx=20, anchor="w")

        self.add_nav_btn(sidebar, "Сейфы", self.show_dashboard)
        self.add_nav_btn(sidebar, "Настройки", self.show_settings)

    def add_nav_btn(self, master, text, command):
        btn = ctk.CTkButton(
            master,
            text=text,
            fg_color="transparent",
            anchor="w",
            height=40,
            hover_color=COLORS["surface"],
            text_color=COLORS["text"],
            command=command
        )
        btn.pack(fill="x", padx=16, pady=6)

    def show_dashboard(self):
        self.clear_main()

        ctk.CTkLabel(
            self.main_container,
            text="Ваши пароли",
            font=("Segoe UI", 30, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(0, 6))

        ctk.CTkLabel(
            self.main_container,
            text="Локальное шифрованное хранилище",
            font=("Segoe UI", 13),
            text_color=COLORS["muted"]
        ).pack(anchor="w", pady=(0, 18))

        editor = ctk.CTkFrame(self.main_container, fg_color=COLORS["surface"], corner_radius=12)
        editor.pack(fill="x", pady=(0, 14))

        self.title_entry = ctk.CTkEntry(editor, placeholder_text="Сервис", width=220, height=38)
        self.title_entry.pack(side="left", padx=(14, 8), pady=14)

        self.login_entry = ctk.CTkEntry(editor, placeholder_text="Логин", width=280, height=38)
        self.login_entry.pack(side="left", padx=8, pady=14)

        AnimatedButton(editor, text="Добавить", width=120, command=self.add_entry).pack(side="left", padx=8)
        ctk.CTkButton(
            editor,
            text="Удалить последний",
            width=140,
            height=42,
            fg_color="transparent",
            hover_color=COLORS["card"],
            text_color=COLORS["muted"],
            command=self.delete_last_entry
        ).pack(side="left", padx=(4, 12))

        self.status_label = ctk.CTkLabel(self.main_container, text="", text_color=COLORS["success"], font=("Segoe UI", 12))
        self.status_label.pack(anchor="w", pady=(0, 10))

        list_wrap = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        list_wrap.pack(fill="both", expand=True)

        if not self.entries:
            ctk.CTkLabel(
                list_wrap,
                text="Пока нет записей. Добавьте первую сверху.",
                text_color=COLORS["muted"],
                font=("Segoe UI", 13)
            ).pack(anchor="w", pady=6)

        for entry in self.entries:
            VaultCard(list_wrap, entry.get("title", "Service"), entry.get("login", "")).pack(fill="x", pady=6)

    def add_entry(self):
        title = self.title_entry.get().strip()
        login = self.login_entry.get().strip()

        if not title or not login:
            self.status_label.configure(text="Заполните сервис и логин", text_color="#FF7B7B")
            return

        self.entries.append({"title": title, "login": login})
        DataManager.save_entries(self.entries)
        self.status_label.configure(text="Запись добавлена", text_color=COLORS["success"])
        self.show_dashboard()

    def delete_last_entry(self):
        if not self.entries:
            self.status_label.configure(text="Список уже пуст", text_color="#FF7B7B")
            return

        self.entries.pop()
        DataManager.save_entries(self.entries)
        self.status_label.configure(text="Последняя запись удалена", text_color=COLORS["success"])
        self.show_dashboard()

    def show_settings(self):
        self.clear_main()

        ctk.CTkLabel(
            self.main_container,
            text="Настройки",
            font=("Segoe UI", 28, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(0, 10))

        card = ctk.CTkFrame(self.main_container, fg_color=COLORS["surface"], corner_radius=14)
        card.pack(fill="x", pady=12)

        ctk.CTkLabel(
            card,
            text="Привязка к HW-ключу",
            font=("Segoe UI", 14, "bold"),
            text_color=COLORS["text"]
        ).pack(side="left", padx=18, pady=16)

        ctk.CTkSwitch(card, text="Активно").pack(side="right", padx=18, pady=14)

        AnimatedButton(self.main_container, text="Сохранить настройки").pack(anchor="w", pady=12)

    def clear_main(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
