import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

from config.paths import get_poster_path
from data.movie_data import get_movie_details
from ui.video_player import VideoPlayer
from utils.image_handler import load_image_for_poster
from services.movie_service import WatchlistService


class MovieDetailPage(tk.Toplevel):
    def __init__(self, poster_filename, main_page, watchlist_service: WatchlistService):
        super().__init__(main_page)
        self.geometry("1000x600")
        self.title("Movie Detail")
        self.poster_filename = poster_filename
        self.main_page = main_page
        self.watchlist_service = watchlist_service

        self.transient(main_page)
        self.grab_set()
        self.configure(bg="#2a2d2e")

        self.movie_title = os.path.splitext(poster_filename)[0]
        self.movie_details = get_movie_details(self.movie_title)

        self.create_widgets()
        self.update_watchlist_button_state()
        self.wait_window()

    def create_widgets(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.left_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(20, 10))

        self.photo = None
        full_poster_path = get_poster_path(self.poster_filename)
        try:
            image = load_image_for_poster(
                full_poster_path, (None, 450)
            )  # Resize by height
            self.photo = ImageTk.PhotoImage(image)
            self.poster_label = ctk.CTkLabel(self.left_frame, image=self.photo, text="")
            self.poster_label.pack(pady=20)
        except Exception as e:
            print(f"Error loading poster: {e}")
            self.poster_label = ctk.CTkLabel(
                self.left_frame,
                text="Poster Not Found",
                font=("Helvetica", 16),
                width=300,
                height=450,
            )
            self.poster_label.pack(pady=20)

        self.right_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 20))

        ctk.CTkLabel(
            self.right_frame, text=self.movie_title, font=("Helvetica", 24, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.info_frame = ctk.CTkFrame(self.right_frame)
        self.info_frame.pack(fill="both", expand=True, pady=(0, 20))

        ctk.CTkLabel(
            self.info_frame,
            text=f"Genre: {self.movie_details['genre']}",
            font=("Helvetica", 14),
        ).pack(anchor="w", padx=10, pady=(10, 5))

        synopsis_text = f"Synopsis:\n{self.movie_details['synopsis']}"
        ctk.CTkLabel(
            self.info_frame,
            text=synopsis_text,
            font=("Helvetica", 12),
            wraplength=350,
            justify="left",
        ).pack(anchor="w", padx=10, pady=5)

        self.action_frame = ctk.CTkFrame(self.right_frame)
        self.action_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            self.action_frame,
            text=f"Rating: {self.movie_details['rating']}",
            font=("Helvetica", 16, "bold"),
        ).pack(side="left", padx=5)

        self.buttons_frame = ctk.CTkFrame(self.action_frame, fg_color="transparent")
        self.buttons_frame.pack(side="right", padx=10)

        self.watchlist_button = ctk.CTkButton(
            self.buttons_frame,
            text="",
            state="normal",
            command=self.add_to_watchlist,
            width=100,
        )
        self.watchlist_button.pack(side="left", padx=5)

        ctk.CTkButton(
            self.buttons_frame,
            text="Watch Trailer",
            command=self.open_trailer,
            width=100,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            self.right_frame, text="Back to Main", command=self.destroy, width=100
        ).pack(anchor="w")

    def update_watchlist_button_state(self):
        if self.watchlist_service.is_in_watchlist(self.poster_filename):
            self.watchlist_button.configure(text="In Watchlist", state="disabled")
        else:
            self.watchlist_button.configure(text="Add to Watchlist", state="normal")

    def add_to_watchlist(self):
        self.main_page.add_to_watchlist(self.poster_filename)
        self.update_watchlist_button_state()

    def open_trailer(self):
        video_player = VideoPlayer(self, self.movie_title)
