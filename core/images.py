import logging
from io import BytesIO

from PIL import Image

from core import MEDIUM_IMG_SIZE, LARGE_IMG_SIZE, SMALL_IMG_SIZE, WEBSERVICE_ENDPOINT
from core.external_resources import fetch_images_json, create_img_dict, get_local_image_path, fetch_image
from db import images_db

logger = logging.getLogger('resizephotos')
logger.setLevel(logging.INFO)


class ResizedPhoto:
    """
    Class used to get all images from the webservice endpoint
    """
    def __init__(self):
        images_urls = fetch_images_json(WEBSERVICE_ENDPOINT)
        self.images_dict = create_img_dict(images_urls)
        self.images_cache = {}  # dictionary that works as cache for images (bytes)

    def get_small_image(self, image_name):
        logger.info("Getting small image: %s", image_name)
        return self._get_resized_image(image_name)

    def get_medium_image(self, image_name):
        logger.info("Getting medium image: %s", image_name)
        return self._get_resized_image(image_name, size=MEDIUM_IMG_SIZE)

    def get_large_image(self, image_name):
        logger.info("Getting large image: %s", image_name)
        return self._get_resized_image(image_name, size=LARGE_IMG_SIZE)

    def _get_resized_image(self, image_name, size=SMALL_IMG_SIZE):
        image_name_resized = "{}_{}_{}".format(size[0], size[1], image_name)
        image_path_resized = get_local_image_path(image_name_resized)

        if image_name_resized in self.images_cache:
            logger.info('Image %s (%s, %s) found in cache', image_name, str(size[0]), str(size[1]))
            image_bytes = self.images_cache[image_name_resized]
        else:
            # look for image in the database
            image_bytes = images_db.find_image(image_name_resized)

        if image_bytes:
            with open(image_path_resized, 'wb') as f:
                Image.open(BytesIO(image_bytes)).save(f)
        else:
            # image not in cache not in the database - image never retrieved before
            local_image = self._get_image_from_endpoint(image_name)

            logger.info('Resizing image to: %s', str(size))
            image = Image.open(local_image)
            image.thumbnail(size, Image.LANCZOS)

            bytes = BytesIO()
            image.save(bytes, format='JPG')
            image_bytes = bytes.getvalue()

            # creating a new image of the desired size (small, medium or large)
            with open(image_path_resized, 'wb') as f:
                image.save(f)

            # image not exist in the database yet, so save it
            images_db.save_image(image_name_resized, image_path_resized)

        # updating cache
        self.images_cache[image_name_resized] = image_bytes

        return image_path_resized

    def _get_image_from_endpoint(self, image_name):
        """
        Get an image from external endpoint based on its name
        :param image_name: name of the image to get
        :return: image filename locally
        """
        logger.info('Getting image from endpoint')

        if image_name not in self.images_dict:
            logger.error("Image %s no found", image_name)
            raise Exception('Image Not Found')

        image_url = self.images_dict[image_name]
        return fetch_image(image_name, image_url)
