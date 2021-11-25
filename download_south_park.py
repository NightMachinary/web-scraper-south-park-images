from brish import *
import os
import re
import requests
from bs4 import BeautifulSoup
import urllib.request
from IPython import embed

BASE_CHAR_PAGE = 'https://southpark.fandom.com/wiki/Portal:Characters'
BASE_DOWNLOAD_DIR = '/Volumes/hyper-diva/archives/image datasets/South Park'
z('mkdir -p {BASE_DOWNLOAD_DIR}').assert_zero
BASE_DOWNLOAD_PATH = BASE_DOWNLOAD_DIR + '/{number}_{name}.{imgformat}'

def download_image(url, current_index, format):
    try:
        name = z('ec "${{$(url-tail {url}):r}}"').assert_zero.outrs
        download_path = BASE_DOWNLOAD_PATH.format(number=current_index,
                                                  name=name,
                                                  imgformat=format)
        urllib.request.urlretrieve(url, download_path)
    except Exception as e:
        print("Couldn't download image " + url)
        print(e)

def get_all_image_urls():
    all_urls = []
    response = requests.get(BASE_CHAR_PAGE)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    urls = [img['src'] for img in img_tags]
    for url in urls:
        if "https://static.wikia.nocookie.net/southpark/images/" in url and "revision" in url:
            short_url = url.split("/revision")[0]
            all_urls.append(short_url)
    return all_urls

def download_all_images():
    all_urls = get_all_image_urls()
    i = 0
    for url in all_urls:
        if "jpeg" in url:
            download_image(url, i, "jpeg")
        else:
            download_image(url, i, "png")
        i = i + 1

download_all_images()

