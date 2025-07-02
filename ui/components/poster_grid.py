import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk
import os

from config.paths import get_poster_path
from utils.image_handler import load_image_for_poster


class PosterGridComponent:
    def __init__(self, parent, on_poster_click_callback):
        self.parent = parent
        self.on_poster_click_callback = on_poster_click_callback
        self._image_cache = {}
        self._scroll_timer = None

        self.container_frame = None
        self.canvas = None
        self.scrollbar = None
        self.scrollable_frame = None
        self.canvas_window = None
        self._last_width = None

        self._create_widgets()

    def _create_widgets(self):
        self.container_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.container_frame.pack(fill="both", expand=True, padx=20)

        self.canvas = tk.Canvas(
            self.container_frame, bg="#1a1b1c", highlightthickness=0
        )
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.scrollbar = ctk.CTkScrollbar(
            self.container_frame, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#2a2d2e")
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self._delayed_scroll_region()
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_width(),
        )

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Extend tk.Canvas with create_rounded_rectangle
        tk.Canvas.create_rounded_rectangle = self._create_rounded_rectangle

    def _create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def _delayed_scroll_region(self):
        if hasattr(self, "_scroll_timer") and self._scroll_timer is not None:
            self.parent.after_cancel(self._scroll_timer)
        self._scroll_timer = self.parent.after(
            100, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def _on_canvas_configure(self, event):
        if self._last_width != event.width:
            self._last_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            self._draw_rounded_corners(event)

    def _draw_rounded_corners(self, event):
        self.canvas.delete("rounded_rect")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        radius = 15
        self.canvas.create_rounded_rectangle(
            2,
            2,
            width - 2,
            height - 2,
            radius=radius,
            fill="#1a1b1c",
            tags="rounded_rect",
        )

    def _on_poster_enter(self, event):
        event.widget.configure(cursor="hand2")

    def _on_poster_leave(self, event):
        event.widget.configure(cursor="")

    def clear_posters(self):
        """Clear all posters from the grid"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def populate_posters(self, poster_list):
        """Populate the grid with posters"""
        self.clear_posters()
        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        BATCH_SIZE = 4
        for i in range(0, len(poster_list), BATCH_SIZE):
            batch = poster_list[i : i + BATCH_SIZE]
            self.parent.after(
                i * 50, lambda x=i, b=batch: self._load_poster_batch(x, b)
            )

    def _load_poster_batch(self, start_index, batch):
        """Load a batch of posters"""
        for index, poster_filename in enumerate(batch):
            full_poster_path = get_poster_path(poster_filename)
            try:
                if full_poster_path not in self._image_cache:
                    image = load_image_for_poster(full_poster_path, (250, 350))
                    self._image_cache[full_poster_path] = ImageTk.PhotoImage(image)

                photo = self._image_cache[full_poster_path]
                poster_frame = ctk.CTkFrame(
                    self.scrollable_frame, fg_color="transparent"
                )

                poster_label = ctk.CTkLabel(poster_frame, image=photo, text="")
                poster_label.image = photo
                poster_label.bind(
                    "<Button-1>",
                    lambda e, path=poster_filename: self.on_poster_click_callback(path),
                )
                poster_label.bind("<Enter>", self._on_poster_enter)
                poster_label.bind("<Leave>", self._on_poster_leave)
                poster_label.pack()

                title = os.path.splitext(poster_filename)[0]
                title_label = ctk.CTkLabel(
                    poster_frame, text=title, font=("Helvetica", 12)
                )
                title_label.pack(pady=2)

                row, col = divmod(start_index + index, 4)
                poster_frame.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")

            except FileNotFoundError:
                self._create_placeholder(start_index + index, "Poster Missing")
            except Exception as e:
                print(f"Error loading poster {poster_filename}: {e}")
                self._create_placeholder(
                    start_index + index,
                    f"Error: {os.path.splitext(poster_filename)[0]}",
                )

    def _create_placeholder(self, position, text):
        """Create a placeholder for missing posters"""
        placeholder = ctk.CTkLabel(self.scrollable_frame, text=text)
        row, col = divmod(position, 4)
        placeholder.grid(row=row, column=col, padx=15, pady=10)

    def show_no_results(self):
        """Show no results message"""
        self.clear_posters()
        no_results = ctk.CTkLabel(
            self.scrollable_frame, text="No Results Found", font=("Helvetica", 16)
        )
        no_results.grid(row=0, column=0, padx=15, pady=10)
