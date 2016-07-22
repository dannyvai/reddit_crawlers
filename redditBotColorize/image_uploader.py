import pyimgur
import secret_keys

client_id = secret_keys.imgur_client_id
client_secret = secret_keys.imgur_client_secret

client = pyimgur.Imgur(client_id)
#client = ImgurClient(client_id, client_secret)

def upload_image(image_path):
    global client
    print 'Uploding image'
    config= { 
        'album' : None, 
        'name' : 'colorized photo from b&w', 
        'title' : 'colorized photo from b&w',
        'description' : 'colorized photo from b&w'
    }
    res = client.upload_image(image_path)

    if res is None:
        print 'didn\'t manage to uplaod the file'
        return None
    else:
        print 'Your photo is here : ' ,res.link
        return res.link

