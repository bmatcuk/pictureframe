#!/usr/bin/env python3

import argparse
import os
import pathlib
import re
import requests
import sys
import time

sys.path.insert(1, './inky')
from PIL import Image, ImageOps
from dotenv import load_dotenv
from gpiod.line import Value
from inky.auto import auto
from io import BytesIO

load_dotenv()

parser = argparse.ArgumentParser()

parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation")

inky = auto(ask_user=True, verbose=True)

args, _ = parser.parse_known_args()
saturation = args.saturation

# get images
image_dir = './images'
images = list(filter(lambda file: re.match(r'^\d+_.*\.png$', file), os.listdir(image_dir)))
images.sort()

# display an image
# this takes a while, so we do it first while we grab an image for next time
displaying_img = len(images) > 0
if displaying_img:
    print('Displaying image: ' + images[0])
    image = Image.open(os.path.join(image_dir, images[0]))
    try:
        inky.set_image(image, saturation=saturation)
    except TypeError:
        inky.set_image(image)

    inky.show()

# get random images from PhotoPrism
next_image_id = int(re.search(r'\d+', images[-1]).group()) + 1 if len(images) > 0 else 0
photoprism_url = 'http://photoprism.lan:2342'
headers = {'X-Auth-Token': os.environ['PHOTOPRISM_TOKEN']}
params = {
    'q': 'landscape:yes',
    'order': 'random',
    'count': 1,
    'public': 'true',
    'merged': 'true',
}
while len(images) < 6:
    params['count'] = 6 - len(images)

    print('Getting {0} new images...'.format(params['count']))
    request = requests.get(photoprism_url + '/api/v1/photos/view', params, headers=headers)
    response = request.json()

    for new_image in response:
        uid = new_image['UID']
        download_url = new_image['DownloadUrl']

        print('Image found: {0} ({1})'.format(uid, download_url))
        if any(image.endswith(uid) for image in images):
            print(uid + ' is a duplicate')
            continue

        # download the image and resize to fit the screen
        request = requests.get(photoprism_url + download_url, headers=headers)
        image = Image.open(BytesIO(request.content))
        resizedimage = ImageOps.fit(image, inky.resolution)

        # save the file
        filename = '{0}_{1}.png'.format(next_image_id, uid)
        print('Saving to ' + filename)
        resizedimage.save(os.path.join(image_dir, filename))
        images.append(filename)
        next_image_id += 1

if displaying_img:
    # delete the image we displayed
    os.remove(os.path.join(image_dir, images[0]))

    # wait for the screen to finish
    print('Waiting for screen to finish...')
    timeout = 30.0
    t_start = time.time()
    while inky._gpio.get_value(inky.busy_pin) == Value.INACTIVE:
        time.sleep(0.1)
        if time.time() - t_start > timeout:
            warnings.warn(f"Busy Wait: Timed out after {timeout:0.2f}s")
            break
    print('Waited {0}'.format(time.time() - t_start))

print('Done.')
