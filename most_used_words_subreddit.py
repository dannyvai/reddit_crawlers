import operator
import argparse

import praw

parser = argparse.ArgumentParser()
parser.add_argument("--subreddit", help="which subreddit to use", default="funny")
parser.add_argument("-n","--num", help="How many posts to test", default=10)
args = parser.parse_args()


glob_words = {}

def gather_words(text,score):
    global glob_words
    words = text.split(' ')
    for word in words:
        if word in glob_words.keys():
            glob_words[word]+= 1
        else:
            glob_words[word] = 1


r = praw.Reddit(user_agent='my_cool_application')
submissions = r.get_subreddit(args.subreddit).get_hot(limit=int(args.num))

for x in submissions:
    score,text = str(x).split("::")
    score = score.rstrip().lstrip()
    text = text.rstrip().lstrip()
    gather_words(text,score)


sorted_x = sorted(glob_words.items(), key=operator.itemgetter(1))

print sorted_x[-10:]
