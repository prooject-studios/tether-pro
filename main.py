import customtkinter as ctk

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TetherProApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tether Pro — Security Dashboard")
        self.geometry("450x550")
        
        # Переменная для статуса "ключа" (флешки)
        self.is_hardware_key_detected = False 

        self.show_login_frame()

    def show_login_frame(self):
        """Экран входа"""
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="TETHER PRO", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        # Индикатор флешки
        self.status_label = ctk.CTkLabel(
            self.frame, 
            text="🔴 Hardware Key: NOT DETECTED", 
            text_color="red",
            font=("Roboto", 12)
        )
        self.status_label.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Master Password", show="*")
        self.password_entry.pack(pady=12, padx=10, fill="x")

        self.login_button = ctk.CTkButton(self.frame, text="Unlock Vault", command=self.login)
        self.login_button.pack(pady=20, padx=10, fill="x")

        # Кнопка имитации вставки флешки (для теста фронтенда)
        self.test_btn = ctk.CTkButton(
            self.frame, 
            text="Test: Insert Flash", 
            fg_color="gray", 
            command=self.simulate_usb
        )
        self.test_btn.pack(side="bottom", pady=10)

    def simulate_usb(self):
        """Имитация подключения аппаратного ключа"""
        self.is_hardware_key_detected = True
        self.status_label.configure(text="🟢 Hardware Key: READY", text_color="green")

    def login(self):
        """Логика входа (пока заглушка)"""
        pwd = self.password_entry.get()
        
        if not self.is_hardware_key_detected:
            print("Ошибка: Подключите аппаратный ключ!")
            return

        if pwd == "admin": # Временная заглушка
            self.frame.destroy()
            self.show_main_vault()
        else:
            print("Ошибка: Неверный мастер-пароль")

    def show_main_vault(self):
        """Главный экран менеджера паролей"""
        self.geometry("800x600")
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Vault Content", font=("Roboto", 20))
        self.title_label.pack(pady=10)

        # Кнопка добавления нового пароля
        self.add_btn = ctk.CTkButton(self.main_frame, text="+ Add New Credentials", width=200)
        self.add_btn.pack(pady=10)

        # Место под список (пока пустое)
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_frame, label_text="Stored Passwords")
        self.scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

if __name__ == "__main__":
    app = TetherProApp()
    app.mainloop()