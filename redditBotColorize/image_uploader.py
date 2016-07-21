from imgurpython import ImgurClient
import secret_keys

client_id = secret_keys.imgur_client_id
client_secret = secret_keys.imgur_client_secret

client = ImgurClient(client_id, client_secret)

def upload_image(image_path):
    print 'Uploding image'
    res = client.upload_from_path(image_path)
    print 'Your photo is here : ' ,res['link']
    return res['link']
    