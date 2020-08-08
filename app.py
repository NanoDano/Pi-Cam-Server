#!/usr/bin/env python3
import logging
import os
from glob import glob
from os import remove
import datetime
from os.path import getmtime, basename, join
from subprocess import Popen, PIPE
from urllib.parse import unquote
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect
from socket import gethostname
import time

logging.basicConfig(level=logging.INFO)
try:
    from picamera import PiCamera, Color, exc
    PI_CAMERA_AVAILABLE = True
except ModuleNotFoundError:
    logging.error('No picamera module found. Continuing without.')
    PI_CAMERA_AVAILABLE = False

# SETTINGS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMAGE_DIR = os.path.join(BASE_DIR, 'static')
# CLOSE SETTING


app = Flask(__name__)

logging.info('Initializing Pi Cam Server')
logging.info(f'Image directory: {STATIC_IMAGE_DIR}')


def get_image_list():
    """
    :return: List of image names sorted with newest first
    """
    images = glob(os.path.join(STATIC_IMAGE_DIR, "*.jpg"))
    images.sort(key=getmtime, reverse=True)  # Newest on top
    images = map(lambda i: basename(i), images)
    return images


def get_disk_usage():
    du = Popen(['du', '-h', STATIC_IMAGE_DIR], stdout=PIPE)
    du_output = du.communicate()[0].decode('utf8').replace('\n', '<br />')

    df = Popen(["df", "-h"], stdout=PIPE)
    df_output = df.communicate()[0].decode('utf8').replace('\n', '<br />')

    return du_output, df_output


@app.route('/', methods=['POST', 'GET'])
def home():
    hostname = gethostname()

    # If there is no Pi camera available (local dev) always do simple GET returns.
    if request.method == 'GET' or not PI_CAMERA_AVAILABLE:
        return render_template('index.html',
                               hostname=hostname,
                               images=get_image_list(),
                               disk_usage=get_disk_usage())

    # POST method only gets this far
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with PiCamera() as camera:
        camera.annotate_background = Color('green')
        camera.annotate_text = now
        image_name = f'image-{now}.jpg'
        try:
            camera.capture(os.path.join(STATIC_IMAGE_DIR, image_name), quality=15)
        except exc.PiCameraMMALError:  # Sometimes the camera will already be in use from something else
            time.sleep(3)
            try:
                camera.capture((STATIC_IMAGE_DIR, image_name), quality=15)
            except Exception as e:
                app.logger.error('Error taking image.')
    return render_template('index.html',
                           hostname=hostname,
                           images=get_image_list(),
                           image_name=image_name,
                           disk_usage=get_disk_usage())


@app.route('/delete')
def delete_image():
    image_path = unquote(request.args.get('image_path'))
    app.logger.info(image_path)
    remove(join(STATIC_IMAGE_DIR, image_path))
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    # app.run(ssl_context='adhoc',  port=9999, host='localhost', debug=True)
