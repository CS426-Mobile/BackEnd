import os
import requests
from django.conf import settings

default_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/2048px-Default_pfp.svg.png"
# default_image_url = "https://static.vecteezy.com/system/resources/thumbnails/020/765/399/small_2x/default-profile-account-unknown-icon-black-silhouette-free-vector.jpg"

def load_image(image_url, author_name):
    local_filename = f"{author_name}_avatar.jpg"
    local_path = os.path.join(settings.MEDIA_ROOT, 'author_images', local_filename)
    author_image = os.path.join(settings.MEDIA_URL, 'author_images', local_filename)

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    download_image(image_url, local_path)
    return author_image

def download_image(image_url, local_path):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        with open(local_path, 'wb') as file:
            file.write(response.content)
    except requests.RequestException:
        response = requests.get(default_image_url)
        with open(local_path, 'wb') as file:
            file.write(response.content)

def ensure_image_exist(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except requests.RequestException:
        image_url = default_image_url
    return image_url