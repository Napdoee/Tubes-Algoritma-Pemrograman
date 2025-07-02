# FileName: /utils/file_manager.py
import os
import json  # Import the json module


def save_credentials(filename, username, password):
    """Saves username and password to a file."""
    try:
        with open(filename, "w") as f:
            f.write(f"{username}\n{password}")
    except IOError as e:
        print(f"Error saving credentials: {e}")


def load_credentials(filename):
    """Loads username and password from a file."""
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            if len(lines) == 2:
                return lines[0].strip(), lines[1].strip()
    except FileNotFoundError:
        pass
    except IOError as e:
        print(f"Error loading credentials: {e}")
    return None, None


def save_watchlist(filename, watchlist):
    """Saves the watchlist to a file."""
    try:
        with open(filename, "w") as f:
            json.dump(watchlist, f)  # Use json.dump to save the list
    except IOError as e:
        print(f"Error saving watchlist: {e}")


def load_watchlist(filename):
    """Loads the watchlist from a file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)  # Use json.load to load the list
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError as e:
        print(f"Error decoding watchlist file: {e}")
        return []  # Return empty list if file is corrupted
    except IOError as e:
        print(f"Error loading watchlist: {e}")
        return []
