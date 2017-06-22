import logging
from PIL import Image

from core import MEDIUM_IMG_SIZE, LARGE_IMG_SIZE, SMALL_IMG_SIZE
from core.external_resources import fetch_images_json, create_img_dict, get_local_image_path, fetch_image

logger = logging.getLogger('resizephotos')


class ResizedPhoto:
    """
    Class used to get all images from the webservice endpoint
    """
    def __init__(self):
        self.webservice_endpoint = "http://54.152.221.29/images.json"

        images_urls = fetch_images_json(self.webservice_endpoint)
        self.images_dict = create_img_dict(images_urls)

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
        logger.info("Resizing image to: %s", str(size))
        local_image = self._get_image(image_name)

        image = Image.open(local_image)
        image.thumbnail(size, Image.LANCZOS)

        resized_image_path = "{}_{}_{}".format(size[0], size[1], image_name)
        image_resized_path = get_local_image_path(resized_image_path)

        with open(image_resized_path, 'wb') as f:
            image.save(f)

        return image_resized_path

    def _get_image(self, image_name):
        """
        Get an image from external endpoint based on its name
        :param image_name: name of the image to get
        :return: image filename locally
        """
        if image_name not in self.images_dict:
            logger.error("Image %s no found", image_name)
            raise Exception('Image Not Found')

        image_url = self.images_dict[image_name]
        return fetch_image(image_name, image_url)
