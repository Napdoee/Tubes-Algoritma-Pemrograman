import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

from config.paths import get_poster_path
from utils.image_handler import load_image_for_poster


class WatchlistPage(tk.Toplevel):
    def __init__(self, parent, watchlist):
        super().__init__(parent)
        self.geometry("1000x800")
        self.title("Watchlist")
        self.watchlist = watchlist
        self.parent = parent  # Reference to MainPage

        self.configure(bg="#2a2d2e")
        self.transient(parent)
        self.grab_set()

        self.images = {}  # To store PhotoImage references

        self.create_widgets()
        self.display_watchlist()
        self.wait_window()

    def create_widgets(self):
        ctk.CTkLabel(self, text="My Watchlist", font=("Helvetica", 24)).pack(pady=10)
        ctk.CTkButton(self, text="Back to Main", command=self.destroy).pack(pady=5)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def display_watchlist(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.watchlist:
            ctk.CTkLabel(
                self.scrollable_frame, text="Your watchlist is empty", font=("Helvetica", 16)
            ).pack(pady=20)
            return

        grid_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)

        for i, movie_filename in enumerate(self.watchlist):
            try:
                movie_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
                row = i // 3
                col = i % 3
                movie_frame.grid(row=row, column=col, padx=10, pady=10)

                full_poster_path = get_poster_path(movie_filename)
                image = load_image_for_poster(full_poster_path, (150, 225))
                photo = ImageTk.PhotoImage(image)
                self.images[movie_filename] = photo

                img_label = ctk.CTkLabel(movie_frame, image=photo, text="")
                img_label.pack(pady=5)

                title = os.path.splitext(movie_filename)[0]
                ctk.CTkLabel(movie_frame, text=title, font=("Helvetica", 12)).pack(pady=2)

                ctk.CTkButton(
                    movie_frame,
                    text="Remove",
                    command=lambda p=movie_filename: self.remove_movie(p),
                    width=100,
                ).pack(pady=5)

            except Exception as e:
                print(f"Error loading {movie_filename}: {e}")
                ctk.CTkLabel(
                    movie_frame,
                    text=f"Error loading\n{os.path.splitext(movie_filename)[0]}",
                    font=("Helvetica", 12),
                ).pack(pady=10)

    def remove_movie(self, movie_filename):
        if movie_filename in self.watchlist:
            self.watchlist.remove(movie_filename)
            if movie_filename in self.images:
                del self.images[movie_filename]
            self.display_watchlist()
            # Optionally, update the main page's watchlist button if this movie was being viewed
            # This would require passing a callback or direct access to main_page's method
            # For simplicity, we'll just refresh the watchlist page.
