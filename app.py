#!flask/bin/python
import logging

from flask import Flask, jsonify, make_response, send_file

from core import IMG_MIME_TYPE, SMALL_IMG_SIZE, MEDIUM_IMG_SIZE, LARGE_IMG_SIZE
from core.images import ResizedPhoto

app = Flask('resizephotos')

resized_photo = ResizedPhoto()


@app.route('/')
def index():
    return "Hello, Image Resize!"


@app.route('/api/images/', methods=['GET'])
def get_images():
    format_dict = {}

    for image_name, image_url in resized_photo.images_dict.items():
        format_dict[image_name] = {
            'url': image_url,
            'formats': {
                'small': SMALL_IMG_SIZE,
                'medium': MEDIUM_IMG_SIZE,
                'large': LARGE_IMG_SIZE
            }
        }

    return jsonify(format_dict)


@app.route('/api/images/small/<image_name>', methods=['GET'])
def get_small_img(image_name):
    local_small_image = resized_photo.get_small_image(image_name)
    return send_file(local_small_image, mimetype=IMG_MIME_TYPE)


@app.route('/api/images/medium/<image_name>', methods=['GET'])
def get_medium_img(image_name):
    local_medium_image = resized_photo.get_medium_image(image_name)
    return send_file(local_medium_image, mimetype=IMG_MIME_TYPE)


@app.route('/api/images/large/<image_name>', methods=['GET'])
def get_large_img(image_name):
    local_large_image = resized_photo.get_large_image(image_name)
    return send_file(local_large_image, mimetype=IMG_MIME_TYPE)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Page Not found'}), 404)


@app.errorhandler(Exception)
def handle_image_not_found(error):
    app.logger.error(error)
    return make_response(jsonify({'error': 'Image Not found'}), 404)


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(debug=True)
