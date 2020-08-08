# Raspberry Pi Camera Webserver

Features:

x Show image from current camera view
x Stores image on disk
x Show links to old pictures taken
- Button to allow deleting
- Show disk space usage


## Camera notes

Pi Cam v1 - 2592 × 1944
Pi Cam v2 - 3280 × 2464
camera.resolution = (x, y)
camera.brightness = 50  # 0-100, Default: 50
You can use camera.image_effect to apply a particular image effect.
The options are:
none, negative, solarize, sketch, denoise, emboss, oilpaint, hatch, gpen,
pastel, watercolor, film, blur, saturation, colorswap, washedout, posterise,
colorpoint, colorbalance, cartoon, deinterlace1, and deinterlace2. The default is none.

## Image sizes

With default 2592x1944 images,
- 1.9 MB to 3.2 MB
- ~400 images per GB

At 5 minute intervals:
- 360 images per day
- ~1 GB per day

30 days = ~24GB
