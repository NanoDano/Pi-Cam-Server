#!/usr/bin/python
from os import environ
import datetime
from flask import Flask, render_template, request
from socket import gethostname
import time
from picamera import PiCamera, Color, exc
import logging


STATIC_IMAGE_DIR = '/home/pi/Pi-Cam-Server/static/'


logging.basicConfig(level=logging.INFO)
logging.info('Initializing Pi Cam Server')
logging.info(f'Image directory: {STATIC_IMAGE_DIR}')


app = Flask(__name__)

# Pi Cam v1 - 2592 × 1944
# Pi Cam v2 - 3280 × 2464
# camera.resolution = (x, y)
# camera.brightness = 50  # 0-100, Default: 50
# You can use camera.image_effect to apply a particular image effect.
# The options are:
# none, negative, solarize, sketch, denoise, emboss, oilpaint, hatch, gpen,
# pastel, watercolor, film, blur, saturation, colorswap, washedout, posterise,
# colorpoint, colorbalance, cartoon, deinterlace1, and deinterlace2. The default is none.



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', context={'hostname': gethostname()})
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    # app.run(ssl_context='adhoc', port=9999, host='localhost', debug=True)
