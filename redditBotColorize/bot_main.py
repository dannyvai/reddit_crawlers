#built-in libs
import urllib
import requests
import traceback

#downloaded libs
import cv2
import praw
#our files

import colorize
import image_uploader
import secret_keys
import image_downloader

subreddit = 'colorize_bw_photos'

colorize.loadDNN(False)

def download_image(url,filename="temp.jpg"):
    image_name = ''

    if image_downloader.is_supported_image_url(url):
        image_name = image_downloader.get_image_name_from_url(url)
        image_downloader.download_image(url,filename)

    elif image_downloader.is_imgur_url(url,filename):
        image_name = image_downloader.download_image_from_imgur(url)

    return filename
    
def check_condition(c):
    text = c.body
    tokens = text.split()
    if "colorize" in tokens:
        return True

r = praw.Reddit(secret_keys.reddit_bot_user_agent)
r.login(username=secret_keys.reddit_username,password=secret_keys.reddit_user_password)

def bot_action(c, verbose=True, respond=False):

    if verbose:
        img_url = c.link_url
        img_path = download_image(img_url)
        print 'img_path is ',img_path
        img = cv2.imread(img_path)
        if img is not None:
            print 'Image downloaded and is ok'
            coloredImage = colorize.runDNN(img_path)
            #coloredImage = img
            print 'after DNN'
            image_name = img_url.split('/')[-1].lstrip().rstrip()
            print 'Image name is : ', image_name
            cv2.imwrite(image_name,coloredImage)
            print 'Uploading image'
            uploaded_image_link = image_uploader.upload_image(image_name)
            if uploaded_image_link is not None:
                try:
                    res = c.reply('We have colorized your photo! here you go : %s'%uploaded_image_link)
                except:
                    traceback.print_exc()
                    print res

            
for c in praw.helpers.comment_stream(r, subreddit):
    if check_condition(c):
        temp = c
        submission = r.get_submission(submission_id=temp.permalink)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        already_comments = False
        for comment in flat_comments:
            if str(comment.author) == secret_keys.reddit_username:
                already_comments = True
                break
        if not already_comments:
            bot_action(c)
