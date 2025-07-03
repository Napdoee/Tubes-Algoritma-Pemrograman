import customtkinter as ctk
import tkinter as tk
import webbrowser
from tkinter import messagebox

from config.paths import get_youtube_trailer_link


class VideoPlayer(tk.Toplevel):
    def __init__(self, parent, movie_title):
        super().__init__(parent)
        self.geometry("400x300")
        self.title(f"{movie_title} - Trailer")
        self.movie_title = movie_title

        self.configure(bg="#2a2d2e")
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_player)

    def create_widgets(self):
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title label
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"Trailer: {self.movie_title}",
            font=("Helvetica", 18, "bold"),
        )
        title_label.pack(pady=20)

        # Get YouTube link
        youtube_link = get_youtube_trailer_link(self.movie_title)

        if youtube_link:
            # Info label
            info_label = ctk.CTkLabel(
                main_frame,
                text="Click the button below to watch the trailer on YouTube",
                font=("Helvetica", 12),
            )
            info_label.pack(pady=10)

            # YouTube button
            youtube_button = ctk.CTkButton(
                main_frame,
                text="🎬 Watch on YouTube",
                command=lambda: self.open_youtube_trailer(youtube_link),
                width=200,
                height=40,
                font=("Helvetica", 14, "bold"),
            )
            youtube_button.pack(pady=20)

            # Link label (optional, for reference)
            link_label = ctk.CTkLabel(
                main_frame,
                text=f"Link: {youtube_link}",
                font=("Helvetica", 10),
                text_color="#888888",
            )
            link_label.pack(pady=5)

        else:
            # No trailer available
            no_trailer_label = ctk.CTkLabel(
                main_frame,
                text="❌ Trailer not available",
                font=("Helvetica", 16),
                text_color="#ff6b6b",
            )
            no_trailer_label.pack(pady=20)

            # Suggestion label
            suggestion_label = ctk.CTkLabel(
                main_frame,
                text="Try searching for the trailer manually on YouTube",
                font=("Helvetica", 12),
                text_color="#888888",
            )
            suggestion_label.pack(pady=10)

        # Back button
        back_button = ctk.CTkButton(
            main_frame, text="Back", command=self.close_player, width=100
        )
        back_button.pack(pady=20)

    def open_youtube_trailer(self, youtube_link):
        """Open YouTube trailer in default browser"""
        try:
            webbrowser.open(youtube_link)
            # Optional: Show confirmation message
            messagebox.showinfo(
                "Trailer Opened",
                f"The trailer for '{self.movie_title}' has been opened in your default browser.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not open YouTube trailer: {str(e)}")

    def close_player(self):
        """Close the video player window"""
        self.destroy()
