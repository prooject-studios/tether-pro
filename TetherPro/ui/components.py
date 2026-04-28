import customtkinter as ctk

# Глобальная палитра проекта
COLORS = {
    "bg": "#0D1117",
    "sidebar": "#161B22",
    "card": "#21262D",
    "accent": "#58A6FF",
    "success": "#2EA043",
    "text": "#F0F6FC"
}

class AnimatedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(master, 
            corner_radius=8,
            height=40,
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent"],
            text_color=COLORS["bg"],
            hover_color="#1F6FEB",
            **kwargs
        )

class VaultCard(ctk.CTkFrame):
    """Компонент карточки пароля в списке"""
    def __init__(self, master, title, login, **kwargs):
        super().__init__(master, fg_color=COLORS["card"], corner_radius=10, **kwargs)
        
        ctk.CTkLabel(self, text=title, font=("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(self, text=login, text_color="#8B949E").pack(side="left", padx=10)
        
        # Кнопка копирования
        self.copy_btn = ctk.CTkButton(self, text="📋", width=30, fg_color="transparent", 
                                      hover_color="#30363D", text_color=COLORS["accent"])
        self.copy_btn.pack(side="right", padx=10)