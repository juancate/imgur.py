#!/usr/bin/env python

import json
import base64
import requests

import os
import random
import string
import subprocess


config = {}


def copy_link_to_clipboard(link):
    echo = subprocess.Popen(['echo', link], stdout=subprocess.PIPE)
    subprocess.Popen(['xclip'], stdin=echo.stdout, stdout=subprocess.PIPE)
    echo.stdout.close()


def post_image(img):
    headers = {'Authorization': 'Client-ID %s' % (config['client_id'],)}
    response = requests.post(
        'https://api.imgur.com/3/image',
        data={
            'image': img,
            'type': 'base64'
        },
        headers=headers
    )

    json_response = response.json()
    print(json.dumps(json_response, indent=2))
    if response.status_code == 200:
        link = json_response['data']['link']
        copy_link_to_clipboard(link)
        print(link)


def encode_image(file_name):
    try:
        with open(file_name, 'rb') as file_image:
            content = file_image.read()
            image = base64.b64encode(content)
            return image
    except Exception:
        print("Image couldn't be read")
    return None


def take_picture(opt=None):
    def random_string(length=6, chars=string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(length))

    image_name = '/tmp/%s.png' % (random_string(),)
    command = ['scrot'] + opt + [image_name]
    return_code = subprocess.call(command)

    if return_code != 0:
        print('Oops! Something went wrong.')
    else:
        image = encode_image(image_name)
        if image:
            post_image(image)


if __name__ == '__main__':
    import sys
    import getopt
    try:
        real_path = os.path.dirname(os.path.realpath(__file__))
        with open(real_path + '/config.json') as f:
            config = json.load(f)
        args, file_name = getopt.getopt(sys.argv[1:], 'sd:o')
        if ('-o', '') in args:
            image = encode_image(file_name[0])
            post_image(image)
        else:
            take_picture(sys.argv[1:])
    except Exception as e:
        print('Oops! Something went wrong:\n%s' % (e,))
