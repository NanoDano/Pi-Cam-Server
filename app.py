#!/usr/bin/python3
import os
import datetime
from flask import Flask, render_template, request
from picamera import PiCamera, Color, exc
import time

IMAGE_DIR = environ.get('IMAGE_DIR')
if not IMAGE_DIR:
    #raise Exception('No IMAGE_DIR in .env file or environment variables.')
    IMAGE_DIR = '/home/pi/Pi-Cam-Server/static/'



# Default static files dir: static/
# Default templates dir: templates/
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
from socket import gethostname

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
            camera.capture(IMAGE_DIR + image_url, quality=15)
        except exc.PiCameraMMALError as e:
            time.sleep(2)
            try:
                camera.capture(IMAGE_DIR + image_url, quality=15)
            except Exception as e:
                return '<html><body>Error fetching image twice in a row. Try again. <form method="POST"><button type="submit">Get picture</button></form></body></html>'

        return f'<html><body><form method="POST"><button type="submit">Get picture</button></form><img src="/static/image-{now}.jpg" /></body></html>'
    return 'Error'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)



# if __name__ == '__main__':
#     app.run(ssl_context='adhoc', port=9999, host='localhost', debug=True)
