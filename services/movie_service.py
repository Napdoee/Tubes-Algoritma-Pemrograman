import time

from config.paths import POSTER_FILENAMES
from config.settings import WATCHLIST_FILE
from utils.file_manager import load_watchlist, save_watchlist


class MovieService:
    def __init__(self):
        self.all_movies = POSTER_FILENAMES.copy()
        self.timer = 0

    def bubble_sort(self, arr, reverse=False):
        n = len(arr)
        sorted_arr = arr.copy()  # Hindari ubah data asli
        for i in range(n):
            for j in range(0, n - i - 1):
                if (not reverse and sorted_arr[j] > sorted_arr[j + 1]) or (
                    reverse and sorted_arr[j] < sorted_arr[j + 1]
                ):
                    sorted_arr[j], sorted_arr[j + 1] = sorted_arr[j + 1], sorted_arr[j]
        return sorted_arr

    def linear_search(self, arr, target):
        target = target.lower()
        result = []
        for item in arr:
            if target in item.lower():
                result.append(item)
        return result

    def search_movies(self, query):
        start_time = time.perf_counter()
        try:
            if not query:
                result = self.all_movies
            else:
                result = self.linear_search(self.all_movies, query)
            return result
        finally:
            end_time = time.perf_counter()
            self.timer = end_time - start_time
            print(
                f"Execution time (Searching - Linear Search): {self.timer:.6f} seconds"
            )

    def sort_movies(self, sort_type="Default"):
        start_time = time.perf_counter()
        try:
            if sort_type == "Ascending":
                result = self.bubble_sort(self.all_movies, reverse=False)
            elif sort_type == "Descending":
                result = self.bubble_sort(self.all_movies, reverse=True)
            else:
                result = self.all_movies.copy()
            return result
        finally:
            end_time = time.perf_counter()
            self.timer = end_time - start_time
            print(f"Execution time (Sorting - Bubble Sort): {self.timer:.6f} seconds")

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
