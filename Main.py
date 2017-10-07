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

    if os == "linux":
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
    if os == "linux":
        display.stop()
    global data_storage
    data_storage = DataStorage.DataCache(html)

def parse_comment(body, comment):
    words_in_comment = re.sub("[^\w]", " ", body).split()
    count = {}
    for word in words_in_comment:
        results = get_player_stats(word)
        for result in results:
            if result.get_name() in count.keys():
                count[result] += 1
            else:
                count[result] = 0
    stats_to_return = [key for key,value in count.items() if value == max(count.values()) ]
    print("Found " + str(len(stats_to_return)) + " results for " + word)
    #comment.reply(print_stats(results))
    print(print_stats(stats_to_return))

def get_player_stats(name):
    if data_storage is None or data_storage.is_expired():
        new_data_storage()
    stats = data_storage.get_player_stats(name)
    return stats

def print_stats(list_of_stats):
    result = ""
    for stat in list_of_stats:
        result += (print_player_stat(stat) + "\n")
    return result

def print_player_stat(stat):
    if isinstance(stat, SkaterStatistics.SkaterStatistics):
        return (stat.get_name() + " has scored " + str(stat.get_goals()) + " goals and " + str(stat.get_assists()) + " assists in "
                + str(stat.get_games_played()) + " games for the " + stat.get_team() + " this year, for a total of " + str(stat.get_points()) + " points.")
    elif isinstance(stat, GoalieStatistics.GoalieStatistics):
        return stat.get_name() + " has played " + str(stat.get_games_played()) + " games this year for the " + stat.get_team() + \
               ", with a goals against average of " + str(stat.get_gaa()) + " and a " + str(stat.get_save_percentage()) + " save percentage."

#reddit = bot_login()
#while True:
#    run_bot(reddit)

parse_comment("henrik sedin", None)
