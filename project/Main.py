import re
import time

import praw

from project import config, StatFormatter
from project.History import CommentHistory

data_storage = None
comment_history = None

def bot_login():
    reddit = praw.Reddit(username = config.username, password = config.password,
                         client_id = config.client_id, client_secret = config.client_secret,
                         user_agent = "hockeystats_beepboop's hockey stat comment bot v0.1")
    return reddit

def run_bot(reddit):
    comment_history = CommentHistory.CommentHistory()
    for comment in reddit.subreddit('test').comments(limit=25):
        if "!stats" in comment.body:
            if comment_history.should_reply_to_comment(comment.submission.id, comment.id, comment.author.id):
                 parse_comment(re.sub("!stats" , "", comment.body), comment)
                 comment_history.add_comment(comment.submission.id, comment.id, comment.author.id)
        time.sleep(10)

def new_data_storage():
    global data_storage
    data_storage = Scraping.DataCache()

def parse_comment(body, comment):
    # Split the individual words in the comment into a list
    words_in_comment = re.sub("[^\w]", " ", body).split()

    # Number of matches found for each player; we return the player with the most matching words
    # For example, !stats Sedin should return both Sedins but !stats Daniel Sedin would only return Daniel
    count = {}
    for word in words_in_comment:
        results = data_storage.parse_player_stats(word.lower())
        for result in results:
            if result in count.keys():
                count[result] += 1
            else:
                count[result] = 0
    # return only the players with the most matches
    stats_to_return = [key for key,value in count.items() if value == max(count.values())]
    comment.reply(StatFormatter.print_stats(stats_to_return))

#reddit = bot_login()
#while True:
#     run_bot(reddit)

parse_comment((re.sub("!stats", "", "!stats sedin daniel")), None)
