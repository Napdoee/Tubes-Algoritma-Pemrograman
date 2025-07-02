import tkinter as tk
from PIL import Image, ImageTk

from utils.image_handler import load_image_for_background


class BackgroundManager:
    def __init__(self, parent, background_path):
        self.parent = parent
        self.background_path = background_path

        self.original_bg = None
        self.bg_image = None
        self.bg_label = None
        self._image_cache = {}
        self._resize_timer = None
        self._last_size = (800, 500)  # Default size

        self._load_background()

    def _load_background(self):
        """Load the background image"""
        try:
            self.original_bg = load_image_for_background(self.background_path)
            initial_width = self.parent.winfo_width() or 800
            initial_height = self.parent.winfo_height() or 500

            resized_bg = self.original_bg.resize(
                (initial_width, initial_height), Image.Resampling.LANCZOS
            )
            self.bg_image = ImageTk.PhotoImage(resized_bg)

            self.bg_label = tk.Label(self.parent, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.parent.bind("<Configure>", self._debounce_resize)
        except Exception as e:
            print(f"Error loading background: {e}")

    def _debounce_resize(self, event=None):
        """Debounce resize events to improve performance"""
        if hasattr(self, "_resize_timer") and self._resize_timer:
            self.parent.after_cancel(self._resize_timer)
        self._resize_timer = self.parent.after(
            150, lambda: self._resize_background(event)
        )

    def _resize_background(self, event):
        """Resize background image when window is resized"""
        if not self.original_bg:
            return

        new_width = self.parent.winfo_width()
        new_height = self.parent.winfo_height()

        # Skip resize if change is too small
        if (
            abs(new_width - self._last_size[0]) < 20
            and abs(new_height - self._last_size[1]) < 20
        ):
            return

        self._last_size = (new_width, new_height)

        # Use cache to improve performance
        cache_key = f"{new_width}x{new_height}"
        if cache_key not in self._image_cache:
            resized_image = self.original_bg.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )
            self._image_cache[cache_key] = ImageTk.PhotoImage(resized_image)

            # Limit cache size
            if len(self._image_cache) > 5:
                old_keys = list(self._image_cache.keys())[:-5]
                for key in old_keys:
                    del self._image_cache[key]

        self.bg_image = self._image_cache[cache_key]
        self.bg_label.configure(image=self.bg_image)
