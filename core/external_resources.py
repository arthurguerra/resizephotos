import json
from os import path, getcwd, pardir
from urllib.request import urlopen

from core import IMG_LOCAL_DIR


def fetch_images_json(endpoint):
    """
    Gets the list of images urls from a given endpoint
    :param endpoint: url to get the list of images urls from
    :return: list of images urls as JSON
    """
    with urlopen(endpoint) as url:
        images = json.loads(url.read().decode())['images']
        return images


def fetch_image(image_name, image_url):
    """
    Gets the actual image file from a given url and saves it locally.
    :param image_name: name of the image that will be saved locally
    :param image_url: url to get the image from
    """
    local_img_path = get_local_image_path(image_name)

    with urlopen(image_url) as url:
        with open(local_img_path, 'wb') as f:
            f.write(url.read())

    return local_img_path


def get_local_image_path(image_name):
    parent_dir = path.join(getcwd(), pardir)
    local_image_path = path.join(parent_dir, IMG_LOCAL_DIR, image_name)
    return local_image_path


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