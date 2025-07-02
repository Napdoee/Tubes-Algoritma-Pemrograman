from config.paths import POSTER_FILENAMES
from config.settings import WATCHLIST_FILE
from utils.file_manager import load_watchlist, save_watchlist
from utils.timer import ExecutionTimer  # Import ExecutionTimer


class MovieService:
    def __init__(self):
        self.all_movies = POSTER_FILENAMES.copy()
        self.timer = ExecutionTimer()  # Initialize timer

    def search_movies(self, query):
        with self.timer:  # Use timer context manager
            if not query:
                return self.all_movies
            query_lower = query.lower()
            result = [
                filename
                for filename in self.all_movies
                if query_lower in filename.lower()
            ]
        return result

    def sort_movies(self, sort_type="Default"):
        with self.timer:  # Use timer context manager
            if sort_type == "Ascending":
                result = sorted(self.all_movies)
            elif sort_type == "Descending":
                result = sorted(self.all_movies, reverse=True)
            else:  # Default
                result = self.all_movies.copy()
        return result

    def get_all_movies(self):
        """Get all available movies"""
        return self.all_movies.copy()


class WatchlistService:
    def __init__(self):
        self.watchlist = load_watchlist(WATCHLIST_FILE)

    def add_to_watchlist(self, movie_filename):
        """Add a movie to the watchlist"""
        if movie_filename not in self.watchlist:
            self.watchlist.append(movie_filename)
            save_watchlist(WATCHLIST_FILE, self.watchlist)  # Simpan perubahan ke file
            return True
        return False

    def remove_from_watchlist(self, movie_filename):
        """Remove a movie from the watchlist"""
        if movie_filename in self.watchlist:
            self.watchlist.remove(movie_filename)
            save_watchlist(WATCHLIST_FILE, self.watchlist)  # Simpan perubahan ke file
            return True
        return False

    def is_in_watchlist(self, movie_filename):
        """Check if a movie is in the watchlist"""
        return movie_filename in self.watchlist

    def get_watchlist(self):
        """Get the current watchlist"""
        return self.watchlist.copy()

    def clear_watchlist(self):
        """Clear the entire watchlist"""
        self.watchlist.clear()
        save_watchlist(WATCHLIST_FILE, self.watchlist)  # Simpan perubahan ke file
