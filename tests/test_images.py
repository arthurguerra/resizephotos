import os
from os import path, getcwd, remove
from os.path import pardir
from unittest import TestCase, main

from PIL import Image

from core import IMG_LOCAL_DIR, SMALL_IMG_SIZE, MEDIUM_IMG_SIZE, LARGE_IMG_SIZE
from core.images import ResizedPhoto


def clean_up_images():
    """
    Deletes all JPG files from the IMAGES directory for testing
    """
    parent_dir = path.join(getcwd(), pardir)
    image_dir = path.join(parent_dir, IMG_LOCAL_DIR)
    for file in os.listdir(image_dir):
        if file.endswith(".jpg"):
            remove(path.join(image_dir, file))


class TestExternalResources(TestCase):
    """
    Test for all functions that deal with external resources (images)
    """
    def setUp(self):
        clean_up_images()
        self.image_name = 'b737_5.jpg'
        self.rp = ResizedPhoto()

    def tearDown(self):
        clean_up_images()

    def test_resize_photo_small(self):
        image = Image.open(self.rp.get_small_image(self.image_name))
        self.assertEqual(SMALL_IMG_SIZE, image.size)

    def test_resize_photo_medium(self):
        image = Image.open(self.rp.get_medium_image(self.image_name))
        self.assertEqual(MEDIUM_IMG_SIZE, image.size)

    def test_resize_photo_large(self):
        image = Image.open(self.rp.get_large_image(self.image_name))
        self.assertEqual(LARGE_IMG_SIZE, image.size)

if __name__ == '__main__':
    main()
