import logging
from io import BytesIO

from bson import Binary
from pymongo import MongoClient

logger = logging.getLogger('resizephotos')

client = MongoClient()  # Mongo DB running on the localhost interface on port 27017
db = client.resizephotos

IMAGE_RESIZED_FILE = 'image_resized_file'


def save_image(image_name_resized, image_path_resized):
    logger.info('Saving image %s (%s) to DB', image_name_resized, image_path_resized)

    if image_path_resized is None:
        logger.error('Invalid image: file not found locally.')
        raise Exception('Image file not found')

    with open(image_path_resized, 'rb') as f:
        image_resized_bytes = BytesIO(f.read()).getvalue()
        image_resized_file = Binary(image_resized_bytes)

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
