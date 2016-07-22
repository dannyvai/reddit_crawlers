import urllib
import requests
import traceback

from imgurpython import ImgurClient

import secret_keys

imgur_client = None

def init_imgur_client():
    global imgur_client
    imgur_client = ImgurClient(secret_keys.imgur_client_id, secret_keys.imgur_client_secret)

def is_supported_image_url(url):
    image_types = ['jpeg','jpg','png']
    if url.split('.')[-1] in image_types:
        return True
    return False

def is_imgur_url(url):
    return ('imgur' in url and '.' not in url.split('/')[-1])

def download_image_from_imgur(url,filename):
    global imgur_client
    if imgur_client is None:
        init_imgur_client()
    image_id = url.split('/')[-1]
    img = imgur_client.get_image(image_id)
    image_url = img.link
    image_name = get_image_name_from_url(image_url)
    print '=== From IMGUR image_name : %s , image_link : %s'%(image_name,image_url)
    if is_supported_image_url(image_url):
        download_image(image_url,image_name)
        return filename
    return None

def get_image_name_from_url(url):
    if len(url) > 0 and '/' in url:
        return url.split('/')[-1]
    return ''


def download_image(url,filename="temp.jpg"):
    try:
        if 'https' in url:
            r = requests.get(url,verify=False,stream=True)
            with open(filename,'wb') as image_fid:
                image_fid.write(r.content)
                image_fid.close()
        else:    
            urllib.urlretrieve(url,filename)
        return filename
    except:
        traceback.print_exc()
        return None
