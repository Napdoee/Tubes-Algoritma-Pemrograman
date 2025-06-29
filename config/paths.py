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

# Video paths (relative to VIDEOS_DIR)
VIDEO_FILENAMES = {
    "Home Alone": "Home Alone Official Trailer.mp4",
    "insidious": "Insidious (2010) Official Trailer #1 - James Wan Movie HD.mp4",
    "Back to the future": "WhatsApp Video 2021-04-14 at 9.46.39 PM.mp4",  # Assuming this is the correct file name
    "My Neighbour Totoro": "My Neighbor Totoro - Celebrate Studio Ghibli - Official Trailer.mp4",
    "The Greatest Showman": "The Greatest Showman _ Official HD Trailer #1 _ 2017.mp4",
    "Coda": "videoplayback.mp4",  # Assuming this is the correct file name
    "spiderman": "SPIDER-MAN_ NO WAY HOME - Official Trailer (HD).mp4",
}


def get_poster_path(filename):
    return os.path.join(POSTER_IMAGES_DIR, filename)


def get_video_path(movie_title):
    filename = VIDEO_FILENAMES.get(movie_title)
    if filename:
        return os.path.join(VIDEOS_DIR, filename)
    return None
