import operator
import argparse

import praw
import cv2

import image_downloader

parser = argparse.ArgumentParser()
parser.add_argument("--subreddit", help="which subreddit to use", default="funny")
parser.add_argument("-n","--num", help="How many posts to test", default=10)
parser.add_argument("--type", help="What type of posts, hot/new/top", default='hot')
parser.add_argument('--debug', help="Debug",default=False)

args = parser.parse_args()

r = praw.Reddit(user_agent='image downloaded bot')

if args.type == 'new':
    submissions = r.get_subreddit(args.subreddit).get_new(limit=int(args.num))
elif args.type == 'top':
    submissions = r.get_subreddit(args.subreddit).get_top(limit=int(args.num))
else:
    submissions = r.get_subreddit(args.subreddit).get_hot(limit=int(args.num))

def show_image(image_path):
    img = cv2.imread(image_name)
    if img is not None:
        cv2.imshow('downloaded image',img)
        cv2.waitKey(0)

for x in submissions:
    print (x.url)
    url = x.url
    if image_downloader.is_supported_image_url(url):
        image_name = image_downloader.get_image_name_from_url(url)
        image_downloader.download_image(url,image_name)
        if args.debug:
            print '%s downloaded from %s'%(image_name,url)
            show_image(image_name)

#        if args.debug:

    elif image_downloader.is_imgur_url(url):
        image_name = image_downloader.download_image_from_imgur(url)
        if image_name is not None:
            if args.debug:
                print '%s downloaded from %s'%(image_name,url)
                show_image(image_name)
        