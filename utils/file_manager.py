import os
import json


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
            json.dump(watchlist, f)
    except IOError as e:
        print(f"Error saving watchlist: {e}")


def load_watchlist(filename):
    """Loads the watchlist from a file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding watchlist file: {e}")
        return []
    except IOError as e:
        print(f"Error loading watchlist: {e}")
        return []


# New helper functions for JSON operations
def save_json_file(filename, data):
    """Save data to JSON file"""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving JSON file {filename}: {e}")


def load_json_file(filename):
    """Load data from JSON file"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file {filename}: {e}")
        return None
    except IOError as e:
        print(f"Error loading JSON file {filename}: {e}")
        return None
