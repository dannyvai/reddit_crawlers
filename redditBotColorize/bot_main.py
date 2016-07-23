
#built-in libs
import urllib
import requests
import traceback
import argparse
import time

#downloaded libs
import cv2
import praw
#our files

import image_uploader
import secret_keys
import image_downloader
import database

parser = argparse.ArgumentParser()
parser.add_argument("--subreddit", help="which subreddit to use", default="colorize_bw_photos")
parser.add_argument('--usednn', dest="useDNN", action='store_true')
parser.add_argument('--no-dnn', dest="useDNN", action='store_false')
parser.add_argument('--replicate', dest="replicate", action='store_true')

parser.set_defaults(useDNN=True,replicate=False)

args = parser.parse_args()

upload_queue = []
upload_timer = time.time()
upload_timeout = 60*10 #every 10 minutes to send what wasn't sent

database.load_database()

MAX_IMAGE_WIDTH = 1920
MAX_IMAGE_HEIGHT = 1080
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

    elif image_downloader.is_reddit_image(url):
        image_name = image_downloader.download_image(url,filename)
        image_name = filename

    return image_name
    
def check_condition(c):
    text = c.body
    tokens = text.split()
    if "colorizebot" in tokens:
        return True

r = praw.Reddit(secret_keys.reddit_bot_user_agent)
r.login(username=secret_keys.reddit_username,password=secret_keys.reddit_user_password)

def bot_action(c, verbose=True, respond=False):

    if verbose:
        img_url = c.link_url
        img_path = download_image(img_url)
        print 'link is : ', img_url, 'img_path is ',img_path
        img = cv2.imread(img_path)
        if img is not None:
            h,w = (img.shape[0],img.shape[1])
            if h > MAX_IMAGE_HEIGHT or w > MAX_IMAGE_WIDTH:
                print '-----Resizing image!!------'
                ratio = float(w)/float(h)
                if h > MAX_IMAGE_HEIGHT:
                    factor = float(h)/float(MAX_IMAGE_HEIGHT)
                else:
                    factor = float(w)/float(MAX_IMAGE_WIDTH)
                img = cv2.resize(img,None,fx=1/factor, fy=1/factor, interpolation = cv2.INTER_CUBIC)
                print '---- after resize image shape is  ----',img.shape
                cv2.imwrite(img_path,img,[cv2.IMWRITE_JPEG_QUALITY,40])
            #if h > 1080 or w > 1920:
            #    try:
            #        c.reply("Sorry image is too big! we currently only support images as big as 1920x1080")
            #        database.add_to_database(c.id)
            #        database.save_database()
            #    except:
            #        return
            #    return
            #1)Run DNN on the b&w image
            print 'Image downloaded and is ok'
            if useDNN:
                coloredImage = colorize.runDNN(img_path)
            else:
                coloredImage = img
            print 'after DNN'
            image_name = 'colorized_'+img_path
            cv2.imwrite(image_name,coloredImage)

            #2)Upload image
            print 'Uploading image'
            if args.replicate:
                uploaded_image_link = img_url
            else:
                uploaded_image_link = image_uploader.upload_image(image_name)

            #3)Reply to the one who summned the bot
            if uploaded_image_link is not None:
                try:
                    res = c.reply('I am an artificial intelligent bot. This is my attempt to color your image, here you go : %s'%uploaded_image_link)
                    database.add_to_database(c.id)
                    database.save_database()
                except:
                    msg = 'I am an artificial intelligent bot. This is my attempt to color your image, here you go : %s'%uploaded_image_link
                    upload_queue.append((c,msg))
                    traceback.print_exc()


#Main loop the listens to new comments on some subreddit 
for c in praw.helpers.comment_stream(r, subreddit):
    if check_condition(c):
        if not database.is_in_db(c.id):
            submission = r.get_submission(submission_id=c.permalink)
            flat_comments = praw.helpers.flatten_tree(submission.comments)
            already_comments = False
            for comment in flat_comments:
                if str(comment.author) == secret_keys.reddit_username:
                    database.add_to_database(c.id)
                    database.save_database()
                    already_comments = True
                    break
            if not already_comments:
                bot_action(c)
    if (time.time() - upload_timer)  > upload_timeout :
        upload_timer = time.time()
        print "Trying to send a comment"
        try:
            reddit_comment,msg = upload_queue[0]
            print reddit_comment.permalink,msg
            reddit_comment.reply(msg)
            upload_queue.pop()
        except:
            pass
