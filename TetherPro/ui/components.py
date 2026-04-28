import customtkinter as ctk

COLORS = {
    "bg": "#0A1222",
    "sidebar": "#0E182B",
    "surface": "#15233B",
    "card": "#1A2C48",
    "accent": "#52A9FF",
    "accent_hover": "#3B8EE0",
    "success": "#38C172",
    "text": "#EAF1FF",
    "muted": "#9CB0D0"
}


class AnimatedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=10,
            height=42,
            font=("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color="#0A1222",
            **kwargs
        )


class VaultCard(ctk.CTkFrame):
    def __init__(self, master, title, login, **kwargs):
        super().__init__(master, fg_color=COLORS["card"], corner_radius=12, **kwargs)

        text_wrap = ctk.CTkFrame(self, fg_color="transparent")
        text_wrap.pack(side="left", fill="x", expand=True, padx=16, pady=12)

        ctk.CTkLabel(
            text_wrap,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_wrap,
            text=login,
            font=("Segoe UI", 12),
            text_color=COLORS["muted"]
        ).pack(anchor="w", pady=(2, 0))

        self.copy_btn = ctk.CTkButton(
            self,
            text="Copy",
            width=70,
            height=32,
            fg_color="transparent",
            hover_color=COLORS["surface"],
            text_color=COLORS["accent"]
        )
        self.copy_btn.pack(side="right", padx=14)
