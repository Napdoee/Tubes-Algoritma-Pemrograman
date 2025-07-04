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
    "Home Alone": "https://youtu.be/dzdpqRGA1qc?si=zQLzCTO7FbOpWOfl",
    "Back to the future": "https://youtu.be/qvsgGtivCgs?si=PsLuk7yDl3GK1q8v",
    "insidious": "https://youtu.be/zuZnRUcoWos?si=d6ypj49F3Caxf8-N",
    "Coda": "https://youtu.be/0pmfrE1YL4I?si=9B6Rl326XP-UwxtR",
    "The Greatest Showman": "https://youtu.be/EodWwczRIe4?si=UANpP3CjF-ybLDtJ",
    "Tetris": "https://youtu.be/-BLM1naCfME?si=G0gjy963Yx-tnUx_",
    "500 Days of Summer": "https://youtu.be/PsD0NpFSADM?si=l6GbLgC6WrDKNsAr",
    "My Neighbour Totoro": "https://youtu.be/92a7Hj0ijLs?si=LBnutUzxrk6W3s-e",
    "Koe no Katachi": "https://www.youtube.com/watch?v=nfK6UgLra7g",
    "Forrest Gump": "https://youtu.be/bLvqoHBptjg?si=rleX5TKzaZcS82kK",
    "Weathering with You": "https://youtu.be/YAXTn0E-Zgo?si=ZVy18046Uw5evOzw",
    "spiderman": "https://www.youtube.com/watch?v=JfVOs4VSpmA",
    "josee": "https://youtu.be/pyDCubgU57g?si=mORborvQRVS7fAD1",
    "suzume": "https://www.youtube.com/watch?v=5q0qfZLhYd4",
    "maquia": "https://www.youtube.com/watch?v=AEWvRqZQ0RU",
    "clouds": "https://youtu.be/OWEgUhWU4g4?si=taPQDm_8yWxhGChe",
}


def get_poster_path(filename):
    return os.path.join(POSTER_IMAGES_DIR, filename)


def get_youtube_trailer_link(movie_title):
    """Get YouTube trailer link for a movie"""
    return YOUTUBE_TRAILER_LINKS.get(movie_title)
