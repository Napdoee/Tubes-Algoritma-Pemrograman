import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

from config.settings import DEFAULT_GEOMETRY, LOGIN_CREDENTIALS, REMEMBER_ME_FILE
from config.paths import BACKGROUND_IMAGE_PATH
from ui.main_page import MainPage
from utils.image_handler import load_image_for_background
from utils.file_manager import save_credentials, load_credentials
from services.user_service import UserService


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(DEFAULT_GEOMETRY)
        self.title("Login Page")

        # Initialize user service
        self.user_service = UserService()

        self.original_bg = None
        self.bg_image = None
        self.bg_label = None

        self.load_background()
        self.create_login_frame()
        self.load_remembered_credentials()

    def load_background(self):
        try:
            self.original_bg = load_image_for_background(BACKGROUND_IMAGE_PATH)
            self.bg_image = ImageTk.PhotoImage(self.original_bg)

            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.bind("<Configure>", self.resize_background)
        except Exception as e:
            print(f"Error loading background: {e}")

    def resize_background(self, event):
        if self.original_bg:
            new_width = event.width
            new_height = event.height
            resized_image = self.original_bg.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )
            self.bg_image = ImageTk.PhotoImage(resized_image)
            self.bg_label.configure(image=self.bg_image)

    def create_login_frame(self):
        self.login_frame = ctk.CTkFrame(
            self, fg_color=("#ffffff", "#323232"), corner_radius=15
        )
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.login_frame,
            text="Login",
            font=("Helvetica", 24, "bold"),
            text_color="white",
        ).pack(padx=40, pady=25)
        ctk.CTkLabel(
            self.login_frame,
            text="Username",
            font=("Helvetica", 16),
            text_color="white",
        ).pack(padx=40, pady=5)
        self.username_entry = ctk.CTkEntry(
            self.login_frame,
            font=("Helvetica", 16),
            width=300,
            fg_color=("white", "gray20"),
        )
        self.username_entry.pack(padx=40, pady=5)

        ctk.CTkLabel(
            self.login_frame,
            text="Password",
            font=("Helvetica", 16),
            text_color="white",
        ).pack(padx=40, pady=5)
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            font=("Helvetica", 16),
            width=300,
            show="*",
            fg_color=("white", "gray20"),
        )
        self.password_entry.pack(padx=40, pady=5)

        self.remember_me_var = tk.BooleanVar()
        ctk.CTkCheckBox(
            self.login_frame,
            text="Remember Me",
            font=("Helvetica", 12),
            text_color="white",
            variable=self.remember_me_var,
        ).pack(padx=40, pady=10)

        ctk.CTkButton(
            self.login_frame, text="Login", font=("Helvetica", 16), command=self.login
        ).pack(padx=40, pady=20)

    def load_remembered_credentials(self):
        username, password = load_credentials(REMEMBER_ME_FILE)
        if username and password:
            self.username_entry.insert(0, username)
            self.password_entry.insert(0, password)
            self.remember_me_var.set(True)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if LOGIN_CREDENTIALS.get(username) == password:
            # Set current user in user service
            self.user_service.set_current_user(username)

            if self.remember_me_var.get():
                save_credentials(REMEMBER_ME_FILE, username, password)
            print("Login Success", "Welcome, " + username)
            self.destroy()
            self.open_main_page(username)
        else:
            print("Login Failed", "Invalid username or password")

    def open_main_page(self, username):
        main_page = MainPage(self.user_service)
        main_page.mainloop()
