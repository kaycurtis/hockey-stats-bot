import re
import time

import praw
from selenium import webdriver
from pyvirtualdisplay import Display

import CommentHistory
import DataStorage
import config

import sys

from PlayerStatsData import GoalieStatistics,SkaterStatistics

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
    os = sys.platform

    if os == "linux2":
        display = Display(visible=0, size=(800,600))
        display.start()
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=options)
        driver.set_window_size(1366, 768)
    elif os == "darwin":
        driver = webdriver.Safari()
    driver.get("https://www.nhl.com/canucks/stats")
    html = driver.page_source
    driver.quit()
    if os == "linux2":
        display.stop()
    global data_storage
    data_storage = DataStorage.DataCache(html)

def parse_comment(body, comment):
    words_in_comment = re.sub("[^\w]", " ", body).split()
    for word in words_in_comment:
        if word != "stats" and not get_player_stats(word) is None:
            print("Found a match for word" + word)
            comment.reply(print_stats(get_player_stats(word)))

def get_player_stats(name):
    if data_storage is None or data_storage.is_expired():
        new_data_storage()
    stats = data_storage.get_player_stats(name)
    return stats

def print_stats(stats):
    if isinstance(stats, SkaterStatistics.SkaterStatistics):
        return (stats.get_name() + " has scored " + str(stats.get_goals()) + " goals and " + str(stats.get_assists()) + " assists in "
          + str(stats.get_games_played()) + " games for the " + stats.get_team() + " this year, for a total of " + str(stats.get_points()) + " points.")
    elif isinstance(stats, GoalieStatistics.GoalieStatistics):
        return stats.get_name() + " has played " + str(stats.get_games_played()) + " games this year for the " + stats.get_team() + \
               ", with a goals against average of " + str(stats.get_gaa()) + " and a " + str(stats.get_save_percentage()) + " save percentage."

reddit = bot_login()
while True:
    run_bot(reddit)