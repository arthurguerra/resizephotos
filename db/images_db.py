import logging

from bson import Binary
from pymongo import MongoClient

logger = logging.getLogger('resizephotos')

client = MongoClient()  # Mongo DB running on the localhost interface on port 27017
db = client.resizephotos

IMAGE_RESIZED_FILE = 'image_resized_file'


def save_image(image_name_resized, image_bytes):
    logger.info('Saving image %s to DB', image_name_resized)

    image_resized_file = Binary(image_bytes)

    return db.images.insert_one({
        'image_resized_name': image_name_resized,
        'image_resized_file': image_resized_file
    })


def find_image(image_resized_name):
    logger.info("Looking for %s in database", image_resized_name)
    image_doc = db.images.find_one({"image_resized_name": image_resized_name})

    if image_doc is None:
        logger.info('Image %s NOT found in the database', image_resized_name)
        return None

    logger.info('Image %s found in the database', image_resized_name)

    # image bytes
    return image_doc['image_resized_file']
