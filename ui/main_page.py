import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

from config.settings import DEFAULT_GEOMETRY
from config.paths import BACKGROUND_IMAGE_PATH, POSTER_FILENAMES, get_poster_path
from ui.movie_detail import MovieDetailPage
from ui.watchlist import WatchlistPage
from utils.image_handler import load_image_for_background, load_image_for_poster


class MainPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(DEFAULT_GEOMETRY)
        self.title("Main Page")

        self._image_cache = {}
        self._last_width = None
        self._resize_timer = None
        self._scroll_timer = None
        self._last_size = (
            self.winfo_width(),
            self.winfo_height(),
        )  # Initialize _last_size

        self.original_bg = None
        self.bg_image = None
        self.bg_label = None

        self.load_background()
        self.watchlist = []
        self.create_widgets()
        self.after(100, self.populate_posters)

    def load_background(self):
        try:
            self.original_bg = load_image_for_background(BACKGROUND_IMAGE_PATH)
            initial_width = self.winfo_width() or 800
            initial_height = self.winfo_height() or 500
            resized_bg = self.original_bg.resize(
                (initial_width, initial_height), Image.Resampling.LANCZOS
            )
            self.bg_image = ImageTk.PhotoImage(resized_bg)

            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.bind("<Configure>", self.debounce_resize)
        except Exception as e:
            print(f"Error loading background: {e}")

    def debounce_resize(self, event=None):
        if hasattr(self, "_resize_timer") and self._resize_timer:
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(150, lambda: self.resize_background(event))

    def resize_background(self, event):
        if not hasattr(self, "original_bg") or self.original_bg is None:
            return

        new_width = self.winfo_width()
        new_height = self.winfo_height()

        if (
            abs(new_width - self._last_size[0]) < 20
            and abs(new_height - self._last_size[1]) < 20
        ):
            return

        self._last_size = (new_width, new_height)

        cache_key = f"{new_width}x{new_height}"
        if cache_key not in self._image_cache:
            resized_image = self.original_bg.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )
            self._image_cache[cache_key] = ImageTk.PhotoImage(resized_image)

            if len(self._image_cache) > 5:
                old_keys = list(self._image_cache.keys())[:-5]
                for key in old_keys:
                    del self._image_cache[key]

        self.bg_image = self._image_cache[cache_key]
        self.bg_label.configure(image=self.bg_image)

    def create_widgets(self):
        self.search_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2a2d2e")
        self.search_frame.pack(pady=10, padx=20, fill="x")
        self.search_frame.pack_propagate(False)
        self.search_frame.configure(height=50)

        self.search_label = ctk.CTkLabel(
            self.search_frame, text="Search", font=("Helvetica", 16)
        )
        self.search_label.grid(row=0, column=0, padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(
            self.search_frame, font=("Helvetica", 16), width=250
        )
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            font=("Helvetica", 16),
            command=self.search,
        )
        self.search_button.grid(row=0, column=2, padx=10, pady=5)

        self.category_menu = ctk.CTkOptionMenu(
            self.search_frame,
            values=["Default", "Ascending", "Descending"],
            command=self.category,
            font=("Helvetica", 16),
        )
        self.category_menu.set("Default")
        self.category_menu.grid(row=0, column=3, padx=10, pady=5)

        self.watchlist_button = ctk.CTkButton(
            self.search_frame,
            text="Watchlist",
            font=("Helvetica", 16),
            command=self.open_watchlist,
        )
        self.watchlist_button.grid(row=0, column=4, padx=10, pady=5)

        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
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
            "<Configure>", lambda e: self.delayed_scroll_region()
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_width(),
        )

        self.canvas.bind("<Configure>", self.on_canvas_configure)
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

    def delayed_scroll_region(self):
        if hasattr(self, "_scroll_timer") and self._scroll_timer is not None:
            self.after_cancel(self._scroll_timer)
        self._scroll_timer = self.after(
            100, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def on_canvas_configure(self, event):
        if self._last_width != event.width:
            self._last_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            self.draw_rounded_corners(event)

    def draw_rounded_corners(self, event):
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

    def on_enter(self, event):
        event.widget.configure(cursor="hand2")
        # event.widget.configure(width=260, height=360) # This might cause layout issues with grid

    def on_leave(self, event):
        event.widget.configure(cursor="")
        # event.widget.configure(width=250, height=350) # This might cause layout issues with grid

    def populate_posters(self, poster_list=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        posters_to_display = (
            poster_list if poster_list is not None else POSTER_FILENAMES
        )
        BATCH_SIZE = 4
        for i in range(0, len(posters_to_display), BATCH_SIZE):
            batch = posters_to_display[i : i + BATCH_SIZE]
            self.after(i * 50, lambda x=i, b=batch: self.load_poster_batch(x, b))

    def load_poster_batch(self, start_index, batch):
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
                    lambda e, path=poster_filename: self.open_movie_detail(path),
                )
                poster_label.bind("<Enter>", self.on_enter)
                poster_label.bind("<Leave>", self.on_leave)
                poster_label.pack()

                title = os.path.splitext(poster_filename)[0]
                title_label = ctk.CTkLabel(
                    poster_frame, text=title, font=("Helvetica", 12)
                )
                title_label.pack(pady=2)

                row, col = divmod(start_index + index, 4)
                poster_frame.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
            except FileNotFoundError:
                placeholder = ctk.CTkLabel(self.scrollable_frame, text="Poster Missing")
                row, col = divmod(start_index + index, 4)
                placeholder.grid(row=row, column=col, padx=15, pady=10)
            except Exception as e:
                print(f"Error loading poster {poster_filename}: {e}")
                placeholder = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=f"Error: {os.path.splitext(poster_filename)[0]}",
                )
                row, col = divmod(start_index + index, 4)
                placeholder.grid(row=row, column=col, padx=15, pady=10)

    def open_movie_detail(self, poster_filename):
        detail_page = MovieDetailPage(poster_filename, self)
        detail_page.mainloop()

    def add_to_watchlist(self, poster_filename):
        if poster_filename not in self.watchlist:
            self.watchlist.append(poster_filename)
            print(f"Added to watchlist: {poster_filename}")

    def open_watchlist(self):
        watchlist_window = WatchlistPage(self, self.watchlist)

    def search(self):
        search_query = self.search_entry.get().lower()
        matching_posters = [
            filename
            for filename in POSTER_FILENAMES
            if search_query in filename.lower()
        ]
        if matching_posters:
            self.populate_posters(matching_posters)
        else:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            no_results = ctk.CTkLabel(
                self.scrollable_frame, text="No Results Found", font=("Helvetica", 16)
            )
            no_results.grid(row=0, column=0, padx=15, pady=10)

    def category(self, value):
        if value == "Default":
            self.populate_posters(POSTER_FILENAMES)
        elif value == "Ascending":
            sorted_posters = sorted(POSTER_FILENAMES)
            self.populate_posters(sorted_posters)
        elif value == "Descending":
            sorted_posters = sorted(POSTER_FILENAMES, reverse=True)
            self.populate_posters(sorted_posters)
