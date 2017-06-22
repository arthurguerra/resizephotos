from urllib.request import urlopen
import json
from os import path, getcwd, pardir

IMG_LOCAL_DIR = "images"


def get_img_json(endpoint):
    """
    Gets the list of images urls from a given endpoint
    :param endpoint: url to get the list of images urls from
    :return: list of images urls as JSON
    """
    with urlopen(endpoint) as url:
        images = json.loads(url.read().decode())['images']
        return images


def get_img(image_name, image_url):
    """
    Gets the actual image file from a given url and saves it locally.
    :param image_name: name of the image that will be saved locally
    :param image_url: url to get the image from
    """
    parent_dir = path.join(getcwd(), pardir)
    local_img_path = path.join(parent_dir, IMG_LOCAL_DIR, image_name)

    with urlopen(image_url) as url:
        with open(local_img_path, 'wb') as f:
            f.write(url.read())

    return local_img_path


def create_img_dict(images_urls):
    """
    Creates a dictionary for all images urls. This dict maps the image name with
    its respective URL
    :param images_urls: list of image urls
    :return: dictionary mapping the image name with its URL
    """
    img_dict = {}
    for img_url_json in images_urls:
        img_url = img_url_json['url']
        img_name = path.basename(img_url)
        img_dict[img_name] = img_url
    return img_dict


class GetExternalImages:
    """
    Class used to get all images from the webservice endpoint
    """
    def __init__(self):
        self.webservice_endpoint = "http://54.152.221.29/images.json"

        images_urls = get_img_json(self.webservice_endpoint)
        self.images_dict = create_img_dict(images_urls)

    def get_image(self, image_name):
        """
        Get an image from external endpoint based on its name
        :param image_name: name of the image to get
        :return: image filename locally
        """
        if image_name not in self.images_dict:
            raise Exception('Image Not Found')

        image_url = self.images_dict[image_name]
        return get_img(image_name, image_url)
