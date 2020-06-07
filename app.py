#!/usr/bin/python
from glob import glob
from os import environ
import datetime
from os.path import getmtime

from flask import Flask, render_template, request, url_for, redirect
from socket import gethostname
import time
from picamera import PiCamera, Color, exc
import logging

STATIC_IMAGE_DIR = '/home/pi/Pi-Cam-Server/static'

logging.basicConfig(level=logging.INFO)
logging.info('Initializing Pi Cam Server')
logging.info(f'Image directory: {STATIC_IMAGE_DIR}')

app = Flask(__name__)

#app.add_url_rule('/favicon.ico', redirect('/static/favicon.png'))  # url_for('static', filename='favicon.png'))


@app.route('/', methods=['POST', 'GET'])
def index():
    images = glob(STATIC_IMAGE_DIR + "/*.jpg")
    # Oldest files are at the front. Newest files at the end
    images.sort(key=getmtime, reverse=True)

    if request.method == 'GET':
        hostname = gethostname()
        print(f'hostname: {hostname}')
        return render_template('index.html', hostname=hostname, images=images)
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    with PiCamera() as camera:
        camera.annotate_background = Color('green')
        camera.annotate_text = now
        image_url = f'image-{now}.jpg'
        try:
            camera.capture(STATIC_IMAGE_DIR + image_url, quality=15)
        except exc.PiCameraMMALError:
            time.sleep(2)
            try:
                camera.capture(STATIC_IMAGE_DIR + image_url, quality=15)
            except Exception as e:
                return '<html><body>Error fetching image twice in a row. Try again. <form method="POST"><button type="submit">Get picture</button></form></body></html>'

        return f'<html><body><form method="POST"><button type="submit">Get picture</button></form><img src="/static/image-{now}.jpg" /></body></html>'
    return 'Error'


# {{ url_for 'static' 'downloads/test.zip' }}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    # app.run(ssl_context='adhoc', port=9999, host='localhost', debug=True)
