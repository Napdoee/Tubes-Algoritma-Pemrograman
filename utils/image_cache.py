from PIL import Image
from config.paths import get_poster_path


class ImageCache:
    def __init__(self):
        self._cache = {}
        self._default_size = (250, 350)

    def get_poster_image(self, poster_filename):
        """Get cached image or load and cache a new one"""
        if poster_filename not in self._cache:
            self._cache[poster_filename] = self._load_and_cache_image(poster_filename)
        return self._cache[poster_filename]

    def _load_and_cache_image(self, poster_filename):
        try:
            full_path = get_poster_path(poster_filename)
            image = Image.open(full_path)
            return image.resize(self._default_size, Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"Error loading image {poster_filename}: {e}")
            raise

    def clear_cache(self):
        """Clear all cached images"""
        self._cache = {}
