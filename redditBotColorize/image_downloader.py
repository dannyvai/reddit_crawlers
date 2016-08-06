#Standard imports
import urllib
import requests
import traceback
import sys
import random

#Downloaded imports
import pyimgur
#Our import
import secret_keys

client_id = secret_keys.imgur_client_id
imgur_client = None
secret_album = None

def init_imgur_client():
    global imgur_client,secret_album
    imgur_client = pyimgur.Imgur(client_id)
    secret_album = imgur_client.get_album(secret_keys.imgur_secret_album_id)


def is_supported_image_url(url):
    image_types = ['jpeg','jpg','png']
    if url.split('.')[-1].split('?')[0].lower() in image_types:
        return True
    return False

def is_imgur_image_url(url):
    return (
            'imgur' in url and 
            '/a/' not in url and #not an album 
            '.' not in url.split('/')[-1] #no extension
    )

def is_imgur_album_url(url):
    return (
            'imgur' in url and 
            '/a/' in url and #not an album 
            '.' not in url.split('/')[-1] #no extension
    )


def is_imgur_album_with_one_picture(url):
    global imgur_client

    if imgur_client is None:
        init_imgur_client()

    if is_imgur_album_url(url):
        album_id = url.split('/')[-1]
        print 'Album',album_id,url

        try:
            album =  imgur_client.get_album(album_id)
        except:
            print 'Exception getting imgur album images %s'%album_id
            traceback.print_exc(file=sys.stdout)
            album = None

        #TODO:: need to check if only one image
        #but for now we just use the first image
        if album is not None and len(album.images) > 0:
            return True
        return False
    return False
        

def is_reddit_image(url):
    return 'https://i.reddituploads.com' in url

def download_image_from_imgur(url):
    global imgur_client
    if imgur_client is None:
        init_imgur_client()

    #image-id could be /image_id?something
    image_id = url.split('/')[-1].split('?')[0] 
    try:
        img = imgur_client.get_image(image_id)
        image_url = img.link
        image_name = get_image_name_from_url(image_url)
        print '=== From IMGUR image_name : %s , image_link : %s'%(image_name,image_url)
        if is_supported_image_url(image_url):
            download_image(image_url,image_name)
            return image_name
    except: 
        print 'Error getting %s' % image_id

    return ''

#
#TODO
#For now this only downloaded the first image in the album
#Needs to download all of them and create an album accordingly
#But for that a code refactor should be done
def download_album_from_imgur(url):
    global imgur_client
    if imgur_client is None:
        init_imgur_client()
    album_id = url.split('/')[-1]

    try:
        album_images = imgur_client.get_album(album_id).images
    except:
        album_images = []

    if len(album_images) > 0:
        image_url = album_images[0].link
        image_name = get_image_name_from_url(image_url)
        download_image(image_url,image_name)
        return image_name

    return ''

def get_image_name_from_url(url):
    if len(url) > 0 and '/' in url:
        return url.split('/')[-1]
    return ''


def download_simple_image(url,filename="temp.jpg"):
    try:
        if 'https' in url:
            r = requests.get(url,verify=True,stream=True)
            with open(filename,'wb') as image_fid:
                image_fid.write(r.content)
                image_fid.close()
        else:    
            urllib.urlretrieve(url,filename)
        return filename
    except:
        traceback.print_exc()
        return ''

def download_image(url,filename="temp.jpg"):
    image_name = ''

    if is_supported_image_url(url):
        image_name = get_image_name_from_url(url)
        download_simple_image(url,filename)
        image_name = filename

    elif is_imgur_image_url(url):
        image_name = download_image_from_imgur(url)

    elif is_imgur_album_with_one_picture(url):
        image_name = download_album_from_imgur(url)

    elif is_reddit_image(url):
        image_name = download_simple_image(url,filename)
        image_name = filename

    return image_name

def get_secret_image_url():
    global secret_album,imgur_client

    if imgur_client is None:
        init_imgur_client()

    return secret_album.images[int(random.uniform(0,len(secret_album.images)))].link
