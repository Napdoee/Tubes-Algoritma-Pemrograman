import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Assets paths
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
VIDEOS_DIR = os.path.join(ASSETS_DIR, "videos")

# Image subdirectories
BACKGROUND_IMAGES_DIR = os.path.join(IMAGES_DIR, "background")
POSTER_IMAGES_DIR = os.path.join(IMAGES_DIR, "posters")

# Specific file paths
BACKGROUND_IMAGE_PATH = os.path.join(BACKGROUND_IMAGES_DIR, "netflix_background.jpg")

# Poster paths (relative to POSTER_IMAGES_DIR)
POSTER_FILENAMES = [
    "Home Alone.jpg",
    "Back to the future.jpg",
    "insidious.jpg",
    "Coda.jpg",
    "The Greatest Showman.jpg",
    "Tetris.jpg",
    "500 Days of Summer.jpg",
    "My Neighbour Totoro.jpg",
    "Koe no Katachi.jpg",
    "Forrest Gump.jpg",
    "Weathering with You.jpg",
    "spiderman.jpg",
    "josee.jpg",
    "suzume.jpg",
    "maquia.jpg",
    "clouds.jpg",
]

# YouTube trailer links
YOUTUBE_TRAILER_LINKS = {
    "Home Alone": "https://www.youtube.com/watch?v=jdRCNM2k42o",
    "Back to the future": "https://www.youtube.com/watch?v=qvsgGtivCgs",
    "insidious": "https://www.youtube.com/watch?v=zuZnRUcoWos",
    "Coda": "https://www.youtube.com/watch?v=o-Uv9W5qtag",
    "The Greatest Showman": "https://www.youtube.com/watch?v=AXCTMGYUg9A",
    "Tetris": "https://www.youtube.com/watch?v=LeAltgu_pbM",
    "500 Days of Summer": "https://www.youtube.com/watch?v=PsD0NpFSADM",
    "My Neighbour Totoro": "https://www.youtube.com/watch?v=92a7Hj0ijLs",
    "Koe no Katachi": "https://www.youtube.com/watch?v=nfK6UgLra7g",
    "Forrest Gump": "https://www.youtube.com/watch?v=bLvqoHBptjg",
    "Weathering with You": "https://www.youtube.com/watch?v=Q6iK6DjV_f8",
    "spiderman": "https://www.youtube.com/watch?v=JfVOs4VSpmA",
    "josee": "https://www.youtube.com/watch?v=mOZ2-WbYXbQ",
    "suzume": "https://www.youtube.com/watch?v=5q0qfZLhYd4",
    "maquia": "https://www.youtube.com/watch?v=AEWvRqZQ0RU",
    "clouds": "https://www.youtube.com/watch?v=oKdIrUyoy5c",
}


def get_poster_path(filename):
    return os.path.join(POSTER_IMAGES_DIR, filename)


def get_youtube_trailer_link(movie_title):
    """Get YouTube trailer link for a movie"""
    return YOUTUBE_TRAILER_LINKS.get(movie_title)
