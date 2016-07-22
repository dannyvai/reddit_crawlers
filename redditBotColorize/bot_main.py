
#built-in libs
import urllib
import requests
import traceback
import argparse

#downloaded libs
import cv2
import praw
#our files

import image_uploader
import secret_keys
import image_downloader

parser = argparse.ArgumentParser()
parser.add_argument("--subreddit", help="which subreddit to use", default="colorize_bw_photos")
parser.add_argument('--usednn', dest="useDNN", action='store_true')
parser.add_argument('--no-dnn', dest="useDNN", action='store_false')
parser.set_defaults(useDNN=True)

args = parser.parse_args()


print args
useDNN = args.useDNN
subreddit = args.subreddit

if useDNN:
    import colorize
    colorize.loadDNN(False)

def download_image(url,filename="temp.jpg"):
    image_name = ''

    if image_downloader.is_supported_image_url(url):
        image_name = image_downloader.get_image_name_from_url(url)
        image_downloader.download_image(url,filename)
        image_name = filename

    elif image_downloader.is_imgur_image_url(url):
        image_name = image_downloader.download_image_from_imgur(url)

    return image_name
    
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
            if useDNN:
                coloredImage = colorize.runDNN(img_path)
            else:
                coloredImage = img
            print 'after DNN'
            image_name = 'colorized_'+img_path
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