import time
from config.paths import POSTER_FILENAMES


class MovieService:
    def __init__(self):
        self.all_movies = POSTER_FILENAMES.copy()
        self.timer = 0

    def bubble_sort(self, arr, reverse=False):
        n = len(arr)
        sorted_arr = arr.copy()
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


# Updated WatchlistService - now uses UserService
class WatchlistService:
    def __init__(self, user_service):
        self.user_service = user_service

    def add_to_watchlist(self, movie_filename):
        """Add a movie to the current user's watchlist"""
        return self.user_service.add_to_user_watchlist(movie_filename)

    def remove_from_watchlist(self, movie_filename):
        """Remove a movie from the current user's watchlist"""
        return self.user_service.remove_from_user_watchlist(movie_filename)

    def is_in_watchlist(self, movie_filename):
        """Check if a movie is in the current user's watchlist"""
        return self.user_service.is_in_user_watchlist(movie_filename)

    def get_watchlist(self):
        """Get the current user's watchlist"""
        return self.user_service.get_user_watchlist()

    def clear_watchlist(self):
        """Clear the current user's watchlist"""
        return self.user_service.clear_user_watchlist()
