import os


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
