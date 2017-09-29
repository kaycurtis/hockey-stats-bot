from selenium import webdriver
import PlayerStatistics
import DataStorage
import config
import praw
import re
import time
import CommentHistory

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
            if not comment_history.contains_id(comment.id):
                 parse_comment(comment.body, comment)
                 comment_history.add_id(comment.id)
        time.sleep(10)

def new_data_storage():
    driver = webdriver.Safari()
    driver.get("https://www.nhl.com/canucks/stats")
    html = driver.page_source
    driver.quit()
    global data_storage
    data_storage = DataStorage.DataCache(html)

def parse_comment(body, comment):
    words_in_comment = re.sub("[^\w]", " ", body).split()
    for word in words_in_comment[1:]:
        if not get_player_stats(word) is None:
            comment.reply(print_stats(get_player_stats(word)))
            return

def get_player_stats(name):
    if data_storage is None or data_storage.is_expired():
        new_data_storage()
    stats = data_storage.get_player_stats(name)
    return stats

def print_stats(stats):
    return (stats.get_name() + " has scored " + str(stats.get_goals()) + " goals and " + str(stats.get_assists()) + " assists in "
          + str(stats.get_games_played()) + " games for the " + stats.get_team() + " this year, for a total of " + str(stats.get_points()) + " points.")

reddit = bot_login()
while True:
    run_bot(reddit)