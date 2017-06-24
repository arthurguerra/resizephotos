import os
import random
import string
from unittest import TestCase, main
from urllib.error import URLError

from core import WEBSERVICE_ENDPOINT
from core.external_resources import fetch_images_json, fetch_image, create_img_dict
from tests import clean_up_images


class TestExternalResources(TestCase):
    """
    Test for all functions that deal with external resources (images)
    """
    def setUp(self):
        clean_up_images()

        self.image_name_not_exists = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        self.image_url_not_exists = 'http://1.2.3.4/images/'.join(random.choice(string.ascii_letters) for _ in range(5))

        self.image_name = 'b737_5.jpg'
        self.image_url = 'http://54.152.221.29/images/b737_5.jpg'

        self.images_urls = []

        for i in range(1, 4):
            name = 'img{}.jpg'.format(i)
            img_entry = {'url': 'http://localhost/images/{}'.format(name)}
            self.images_urls.append(img_entry)

    def tearDown(self):
        clean_up_images()

    def test_fetch_images_json(self):
        """
        Test fetching images JSON.
        """
        json = fetch_images_json(WEBSERVICE_ENDPOINT)
        self.assertIsNotNone(json)
        self.assertEqual(10, len(json))

    def test_fetch_image_file(self):
        local_image_path = fetch_image(self.image_name, self.image_url)
        self.assertIsNotNone(local_image_path)
        self.assertTrue(os.path.exists(local_image_path))

    def test_fetch_image_file_not_exists(self):
        self.assertRaises(URLError, fetch_image, self.image_name_not_exists, self.image_url_not_exists)

    def test_create_image_dict(self):
        img_dict = create_img_dict(self.images_urls)

        for i in range(1, 4):
            name = 'img{}.jpg'.format(i)
            self.assertTrue(name in img_dict)
            self.assertTrue(img_dict[name].endswith(name))

if __name__ == '__main__':
    main()
