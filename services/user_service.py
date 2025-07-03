import json
import os
from utils.file_manager import load_json_file, save_json_file


class UserService:
    def __init__(self):
        self.users_file = "users_data.json"
        self.current_user = None
        self.users_data = self.__load_users_data()

    def __load_users_data(self):
        """Load users data from file"""
        try:
            return load_json_file(self.users_file) or {}
        except:
            return {}

    def _save_users_data(self):
        """Save users data to file"""
        save_json_file(self.users_file, self.users_data)

    def set_current_user(self, username):
        """Set the current logged-in user"""
        self.current_user = username
        # Initialize user data if doesn't exist
        if username not in self.users_data:
            self.users_data[username] = {
                "watchlist": [],
                "preferences": {},
                "last_login": None,
            }
            self._save_users_data()

    def get_current_user(self):
        """Get current logged-in user"""
        return self.current_user

    def get_user_watchlist(self, username=None):
        """Get watchlist for specific user or current user"""
        user = username or self.current_user
        if user and user in self.users_data:
            return self.users_data[user].get("watchlist", [])
        return []

    def add_to_user_watchlist(self, movie_filename, username=None):
        """Add movie to user's watchlist"""
        user = username or self.current_user
        if not user:
            return False

        if user not in self.users_data:
            self.users_data[user] = {"watchlist": [], "preferences": {}}

        if movie_filename not in self.users_data[user]["watchlist"]:
            self.users_data[user]["watchlist"].append(movie_filename)
            self._save_users_data()
            return True
        return False

    def remove_from_user_watchlist(self, movie_filename, username=None):
        """Remove movie from user's watchlist"""
        user = username or self.current_user
        if not user or user not in self.users_data:
            return False

        if movie_filename in self.users_data[user]["watchlist"]:
            self.users_data[user]["watchlist"].remove(movie_filename)
            self._save_users_data()
            return True
        return False

    def is_in_user_watchlist(self, movie_filename, username=None):
        """Check if movie is in user's watchlist"""
        user = username or self.current_user
        if user and user in self.users_data:
            return movie_filename in self.users_data[user]["watchlist"]
        return False

    def clear_user_watchlist(self, username=None):
        """Clear user's watchlist"""
        user = username or self.current_user
        if user and user in self.users_data:
            self.users_data[user]["watchlist"] = []
            self._save_users_data()
            return True
        return False
