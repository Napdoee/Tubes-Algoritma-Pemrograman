import customtkinter as ctk
import tkinter as tk
import os

# import vlc # Uncomment this line if you have VLC installed and configured

from config.paths import get_video_path


class VideoPlayer(tk.Toplevel):
    def __init__(self, parent, movie_title):
        super().__init__(parent)
        self.geometry("800x600")
        self.title(f"{movie_title} - Trailer")
        self.movie_title = movie_title

        self.configure(bg="#2a2d2e")
        self.transient(parent)
        self.grab_set()

        self.fullscreen = False
        self.player = None  # Initialize player to None

        self.create_widgets()
        self.load_and_play_video()

        self.protocol("WM_DELETE_WINDOW", self.close_player)

    def create_widgets(self):
        self.video_frame = ctk.CTkFrame(self)
        self.video_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.video_canvas = tk.Canvas(self.video_frame, bg="black")
        self.video_canvas.pack(fill="both", expand=True)

        self.bind("<Double-Button-1>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)

        ctk.CTkButton(self, text="Back", command=self.close_player, width=100).pack(pady=10)

    def load_and_play_video(self):
        video_path = get_video_path(self.movie_title)

        # Check if vlc is imported and available
        if "vlc" not in globals():
            error_label = ctk.CTkLabel(
                self.video_canvas,
                text="VLC module not imported. Cannot play video.",
                font=("Helvetica", 16),
            )
            error_label.pack(pady=20)
            print(
                "Error: VLC module not imported. Please uncomment 'import vlc' in ui/video_player.py and ensure VLC is installed."
            )
            return

        try:
            # Initialize VLC instance
            self.instance = vlc.Instance(
                "--no-xlib"
            )  # Add this parameter for Linux/macOS if needed
            self.player = self.instance.media_player_new()

            if video_path and os.path.exists(video_path):
                media = self.instance.media_new(video_path)
                self.player.set_media(media)

                if os.name == "nt":  # Windows
                    self.player.set_hwnd(self.video_canvas.winfo_id())
                else:  # Linux/Mac
                    self.player.set_xwindow(self.video_canvas.winfo_id())

                self.player.play()
            else:
                error_label = ctk.CTkLabel(
                    self.video_canvas,
                    text="Trailer not available or file not found",
                    font=("Helvetica", 16),
                )
                error_label.pack(pady=20)
                print(f"Video file not found for {self.movie_title} at {video_path}")
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.video_canvas,
                text=f"Error initializing video player: {e}",
                font=("Helvetica", 16),
            )
            error_label.pack(pady=20)
            print(f"Error initializing VLC: {e}")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        # Hide/show back button in fullscreen
        if self.fullscreen:
            self.children["!ctkbutton"].pack_forget()  # Access button by its internal name
        else:
            self.children["!ctkbutton"].pack(pady=10)

    def exit_fullscreen(self, event=None):
        if self.fullscreen:
            self.fullscreen = False
            self.attributes("-fullscreen", False)
            self.children["!ctkbutton"].pack(pady=10)

    def close_player(self):
        if self.player:
            self.player.stop()
            self.player.release()  # Release the player
        self.destroy()
