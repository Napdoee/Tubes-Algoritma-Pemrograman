import customtkinter as ctk


class SearchBarComponent:
    def __init__(
        self, parent, on_search_callback, on_category_callback, on_watchlist_callback
    ):
        self.parent = parent
        self.on_search_callback = on_search_callback
        self.on_category_callback = on_category_callback
        self.on_watchlist_callback = on_watchlist_callback

        self.search_frame = None
        self.search_entry = None
        self.category_menu = None
        self.execution_time_label = None  # Add this attribute

        self._create_widgets()

    def _create_widgets(self):
        self.search_frame = ctk.CTkFrame(
            self.parent, corner_radius=10, fg_color="#2a2d2e"
        )
        self.search_frame.pack(pady=10, padx=20, fill="x")
        self.search_frame.pack_propagate(False)
        self.search_frame.configure(height=50)

        search_label = ctk.CTkLabel(
            self.search_frame, text="Search", font=("Helvetica", 16)
        )
        search_label.grid(row=0, column=0, padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(
            self.search_frame, font=("Helvetica", 16), width=250
        )
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)

        search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            font=("Helvetica", 16),
            command=self._on_search,
        )
        search_button.grid(row=0, column=2, padx=10, pady=5)

        self.category_menu = ctk.CTkOptionMenu(
            self.search_frame,
            values=["Default", "Ascending", "Descending"],
            command=self._on_category,
            font=("Helvetica", 16),
        )
        self.category_menu.set("Default")
        self.category_menu.grid(row=0, column=3, padx=10, pady=5)

        watchlist_button = ctk.CTkButton(
            self.search_frame,
            text="Watchlist",
            font=("Helvetica", 16),
            command=self._on_watchlist,
        )
        watchlist_button.grid(row=0, column=4, padx=10, pady=5)

        # New: Label to display execution time
        self.execution_time_label = ctk.CTkLabel(
            self.search_frame,
            text="Time: 0.000s",
            font=("Helvetica", 12),
            text_color="gray",
        )
        self.execution_time_label.grid(row=0, column=5, padx=10, pady=5)

    def _on_search(self):
        query = self.search_entry.get()
        self.on_search_callback(query)  # This callback will update the time label

    def _on_category(self, value):
        self.on_category_callback(value)  # This callback will update the time label

    def _on_watchlist(self):
        self.on_watchlist_callback()

    def get_search_query(self):
        return self.search_entry.get()

    def clear_search(self):
        self.search_entry.delete(0, "end")

    def update_time_label(self, name, time_in_seconds):
        """Updates the time label with the given execution time."""
        self.execution_time_label.configure(
            text=f"Time {f"({name})" if name else ""}: {time_in_seconds:.6f}s"
        )
