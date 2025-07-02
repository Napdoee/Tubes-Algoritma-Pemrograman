# ui/main_page.py
import customtkinter as ctk

from config.settings import DEFAULT_GEOMETRY, WATCHLIST_FILE
from config.paths import BACKGROUND_IMAGE_PATH
from ui.movie_detail import MovieDetailPage
from ui.watchlist import WatchlistPage
from ui.components.search_bar import (
    SearchBarComponent,
)
from ui.components.poster_grid import (
    PosterGridComponent,
)
from ui.components.background import (
    BackgroundManager,
)
from services.movie_service import MovieService, WatchlistService
from utils.file_manager import (
    save_watchlist,
    load_watchlist,
)


class MainPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(DEFAULT_GEOMETRY)
        self.title("Main Page")

        # Initialize services
        self.movie_service = MovieService()
        self.watchlist_service = WatchlistService()
        self.watchlist_service.watchlist = load_watchlist(WATCHLIST_FILE)

        # Initialize components
        self.background_manager = None
        self.search_bar = None
        self.poster_grid = None

        self._setup_window()
        self._create_components()
        self.after(100, self._load_initial_posters)

    def _setup_window(self):
        """Setup the main window with background"""
        self.background_manager = BackgroundManager(self, BACKGROUND_IMAGE_PATH)

    def _create_components(self):
        """Create all UI components"""
        self.search_bar = SearchBarComponent(
            parent=self,
            on_search_callback=self._handle_search,
            on_category_callback=self._handle_category_change,
            on_watchlist_callback=self._open_watchlist,
        )

        self.poster_grid = PosterGridComponent(
            parent=self, on_poster_click_callback=self._open_movie_detail
        )

    def _load_initial_posters(self):
        """Load initial posters on startup"""
        movies = self.movie_service.get_all_movies()
        self.poster_grid.populate_posters(movies)
        # Set initial time to 0.0 as no search/sort operation has occurred yet
        self.search_bar.update_time_label(0.0)

    def _handle_search(self, query):
        """Handle search functionality"""
        if not query.strip():
            movies = self.movie_service.get_all_movies()
            self.poster_grid.populate_posters(movies)
            # When query is empty, reset time to 0.0
            self.search_bar.update_time_label(0.0)
            return

        # Perform search and get execution time
        matching_movies = self.movie_service.search_movies(query)
        execution_time = self.movie_service.timer.last_execution_time

        # Update UI
        if matching_movies:
            self.poster_grid.populate_posters(matching_movies)
        else:
            self.poster_grid.show_no_results()

        # Update time label after search operation
        self.search_bar.update_time_label(execution_time)

    def _handle_category_change(self, category):
        """Handle category/sorting change"""
        # Perform sort and get execution time
        sorted_movies = self.movie_service.sort_movies(category)
        execution_time = self.movie_service.timer.last_execution_time

        # Update UI
        self.poster_grid.populate_posters(sorted_movies)

        # Update time label after sort operation
        self.search_bar.update_time_label(execution_time)

    def _open_movie_detail(self, poster_filename):
        """Open movie detail page"""
        detail_page = MovieDetailPage(poster_filename, self, self.watchlist_service)
        detail_page.mainloop()

    def _open_watchlist(self):
        """Open watchlist page"""
        watchlist_window = WatchlistPage(self, self.watchlist_service)
        watchlist_window.mainloop()

    def add_to_watchlist(self, poster_filename):
        """Add movie to watchlist."""
        if self.watchlist_service.add_to_watchlist(poster_filename):
            save_watchlist(WATCHLIST_FILE, self.watchlist_service.get_watchlist())
            print(f"Added to watchlist: {poster_filename}")

    def remove_from_watchlist(self, poster_filename):
        """Remove movie from watchlist."""
        if self.watchlist_service.remove_from_watchlist(poster_filename):
            save_watchlist(WATCHLIST_FILE, self.watchlist_service.get_watchlist())
            print(f"Removed from watchlist: {poster_filename}")

    @property
    def watchlist(self):
        """Property to maintain backward compatibility and get current watchlist."""
        return self.watchlist_service.get_watchlist()
