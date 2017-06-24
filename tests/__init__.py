from os import path, getcwd, pardir, listdir, remove

from core import IMG_LOCAL_DIR


def clean_up_images():
    """
    Deletes all JPG files from the IMAGES directory for testing
    """
    parent_dir = path.join(getcwd(), pardir)
    image_dir = path.join(parent_dir, 'resizephotos', IMG_LOCAL_DIR)
    for file in listdir(image_dir):
        if file.endswith(".jpg"):
            remove(path.join(image_dir, file))
