class AuthWindow(ctk.CTk):
    def __init__(self, mode="login"):
        super().__init__()
        self.mode = mode
        self.setup_ui()

    def setup_ui(self):
        self.geometry("400x500")
        if self.mode == "register":
            self.title("Tether Pro: Первый запуск")
            self.render_registration()
        else:
            self.title("Tether Pro: Вход")
            self.render_login()

    def render_registration(self):
        ctk.CTkLabel(self, text="ПРИДУМАЙТЕ ПАРОЛЬ", font=("Arial", 18, "bold")).pack(pady=20)
        self.p1 = ctk.CTkEntry(self, placeholder_text="Мастер-пароль", show="*", width=300)
        self.p1.pack(pady=10)
        self.p2 = ctk.CTkEntry(self, placeholder_text="Повторите пароль", show="*", width=300)
        self.p2.pack(pady=10)
        
        ctk.CTkButton(self, text="СОЗДАТЬ ХРАНИЛИЩЕ", command=self.create_vault).pack(pady=20)

    def create_vault(self):
        if self.p1.get() == self.p2.get() and len(self.p1.get()) > 7:
            # Тут вызываем DataManager и Rust-ядро
            self.destroy()
            # Запускаем основное приложение
        else:
            print("Пароли не совпадают или слишком короткие")