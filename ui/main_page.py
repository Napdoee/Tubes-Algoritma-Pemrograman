import customtkinter as ctk

from config.settings import DEFAULT_GEOMETRY
from config.paths import BACKGROUND_IMAGE_PATH
from ui.movie_detail import MovieDetailPage
from ui.watchlist import WatchlistPage
from ui.components.search_bar import SearchBarComponent
from ui.components.poster_grid import PosterGridComponent
from ui.components.background import BackgroundManager
from services.movie_service import MovieService, WatchlistService
from services.user_service import UserService


class MainPage(ctk.CTk):
    def __init__(self, user_service: UserService):
        super().__init__()
        self.geometry(DEFAULT_GEOMETRY)
        self.title(f"Main Page - Welcome {user_service.get_current_user()}")

        # Initialize services
        self.user_service = user_service
        self.movie_service = MovieService()
        self.watchlist_service = WatchlistService(self.user_service)

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
        self.search_bar.update_time_label(False, 0.0)

    def _handle_search(self, query):
        """Handle search functionality"""
        if not query.strip():
            movies = self.movie_service.get_all_movies()
            self.poster_grid.populate_posters(movies)
            self.search_bar.update_time_label(False, 0.0)
            return

        matching_movies = self.movie_service.search_movies(query)
        execution_time = self.movie_service.timer

        if matching_movies:
            self.poster_grid.populate_posters(matching_movies)
        else:
            self.poster_grid.show_no_results()

        self.search_bar.update_time_label("Search", execution_time)

    def _handle_category_change(self, category):
        """Handle category/sorting change"""
        sorted_movies = self.movie_service.sort_movies(category)
        execution_time = self.movie_service.timer
        self.poster_grid.populate_posters(sorted_movies)
        self.search_bar.update_time_label("Sort", execution_time)

    def _open_movie_detail(self, poster_filename):
        """Open movie detail page"""
        detail_page = MovieDetailPage(poster_filename, self, self.watchlist_service)
        detail_page.mainloop()

    def _open_watchlist(self):
        """Open watchlist page"""
        watchlist_window = WatchlistPage(self, self.watchlist_service)
        watchlist_window.mainloop()

    def add_to_watchlist(self, poster_filename):
        """Add movie to user's watchlist."""
        if self.watchlist_service.add_to_watchlist(poster_filename):
            print(
                f"Added to watchlist for {self.user_service.get_current_user()}: {poster_filename}"
            )

    def remove_from_watchlist(self, poster_filename):
        """Remove movie from user's watchlist."""
        if self.watchlist_service.remove_from_watchlist(poster_filename):
            print(
                f"Removed from watchlist for {self.user_service.get_current_user()}: {poster_filename}"
            )

    @property
    def watchlist(self):
        """Property to get current user's watchlist."""
        return self.watchlist_service.get_watchlist()
