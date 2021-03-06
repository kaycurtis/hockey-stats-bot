import re
import time
import logging, logging.handlers

import praw
import prawcore.exceptions
from praw.exceptions import APIException
from requests.exceptions import ReadTimeout

from project import config, StatFormatter
from project.History import CommentHistory
from project.Scraping import DataScraper

data_storage = DataScraper.DataScraper()
comment_history = CommentHistory.CommentHistory()

def get_logger():
    smtp_handler = logging.handlers.SMTPHandler(mailhost=("smtp.gmail.com", 587),
                                                credentials=(config.bot_gmail_username, config.bot_gmail_password),
                                                secure=(),
                                                fromaddr=config.bot_email,
                                                toaddrs=config.dev_email,
                                                subject=u"You messed up :(")
    logger = logging.getLogger()
    logger.addHandler(smtp_handler)
    return logger

def bot_login():
    reddit = praw.Reddit(username = config.username, password = config.password,
                         client_id = config.client_id, client_secret = config.client_secret,
                         user_agent = "hockeystats_beepboop's hockey stat comment bot v0.2")
    return reddit

def run_bot(reddit):
    try:
        for comment in reddit.subreddit('canucks').comments(limit=25):
             if "!stats" in comment.body:
                  if comment_history.should_reply_to_comment(comment):
                      print("Replying to '" + comment.body + "'")
                      parse_comment(re.sub("!stats" , "", comment.body), comment)
                      comment_history.add_comment(comment.submission.id, comment.id, comment.author.id)
    except prawcore.exceptions.ServerError:
        print("Got a 503, gonna sleep for a bit and try again")
        time.sleep(60)
    except ReadTimeout:
        print("Read timeout, sleeping for 30 seconds")
        time.sleep(30)

def parse_comment(body, comment):
    # Split the individual words in the comment into a list
    words_in_comment = re.sub("[^\w]", " ", body).split()

    # Number of matches found for each player; we return the player with the most matching words
    # For example, !stats Sedin should return both Sedins but !stats Daniel Sedin would only return Daniel
    count = {}
    for word in words_in_comment:
        results = data_storage.find_stats_matching_word(word.lower())
        for result in results:
            if result in count.keys():
                count[result] += 1
            else:
                count[result] = 0
    # return only the players with the most matches
    stats_to_return = [key for key,value in count.items() if value == max(count.values())]
    while True:
        try:
            comment.reply(StatFormatter.print_stats(stats_to_return))
            return
        except praw.exceptions.APIException:
            print("Too many api calls, let's sleep for a bit friend")
            time.sleep(600)

reddit = bot_login()
logger = get_logger()
try:
    while True:
        run_bot(reddit)
except Exception as e:
    logger.exception("Unhandled exception")


