from PIL import Image, ImageTk


def load_image_for_background(path):
    """Loads an image for background use."""
    return Image.open(path)


def load_image_for_poster(path, size=(250, 350)):
    """Loads and resizes an image for poster display.
    Size can be (width, height) or (None, height) to maintain aspect ratio.
    """
    image = Image.open(path)
    if size[0] is None:  # Resize by height, maintain aspect ratio
        aspect_ratio = image.width / image.height
        new_height = size[1]
        new_width = int(new_height * aspect_ratio)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:  # Resize to specific width and height
        return image.resize(size, Image.Resampling.LANCZOS)
