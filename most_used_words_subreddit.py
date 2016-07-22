import operator
import argparse

import praw

parser = argparse.ArgumentParser()
parser.add_argument("--subreddit", help="which subreddit to use", default="funny")
parser.add_argument("-n","--num", help="How many posts to test", default=10)
parser.add_argument("--type", help="What type of posts, hot/new/top", default='hot')
args = parser.parse_args()


glob_words = {}

def gather_words(text,score):
    global glob_words
    words = text.split(' ')
    for word in words:
        if word in glob_words.keys():
            glob_words[word]+= score/len(words)
        else:
            glob_words[word] = score/len(words)


r = praw.Reddit(user_agent='my_cool_application')

if args.type == 'new':
    submissions = r.get_subreddit(args.subreddit).get_new(limit=int(args.num))
elif args.type == 'top':
    submissions = r.get_subreddit(args.subreddit).get_top(limit=int(args.num))
else:
    submissions = r.get_subreddit(args.subreddit).get_hot(limit=int(args.num))

for x in submissions:
    score = x.score
    text = x.selftext
    gather_words(text,score)

sorted_x = sorted(glob_words.items(), key=operator.itemgetter(1))
print sorted_x[-20:]
