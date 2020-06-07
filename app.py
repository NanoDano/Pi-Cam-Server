#!/usr/bin/python
from glob import glob
from os import environ, remove
import datetime
from os.path import getmtime, basename, join
from urllib.parse import unquote

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

@app.route('/delete')
def delete_image():
    image_path = unquote(request.args.get('image_path'))
    app.logger.info(image_path)
    remove(join(STATIC_IMAGE_DIR, image_path))
    return redirect(url_for('home'))

@app.route('/', methods=['POST', 'GET'])
def home():
    images = glob(STATIC_IMAGE_DIR + "/*.jpg")
    images.sort(key=getmtime, reverse=True)  # Newest on top
    images = map(lambda i: basename(i), images)

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
