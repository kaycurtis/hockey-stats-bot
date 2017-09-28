import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import datetime
import PlayerStatistics
import DataStorage

data_storage = None

def new_data_storage():
    driver = webdriver.Safari()
    driver.get("https://www.nhl.com/canucks/stats")
    html = driver.page_source
    driver.quit()
    global data_storage
    data_storage = DataStorage.DataCache(html)

def get_player_stats(name):
    if data_storage is None or data_storage.is_expired():
        new_data_storage()
    stats = data_storage.get_player_stats(name)
    print_stats(stats)

def print_stats(stats):
    print(stats.get_name() + " has scored " + str(stats.get_goals()) + " goals and " + str(stats.get_assists()) + " assists in "
          + str(stats.get_games_played()) + " games for the " + stats.get_team() + " this year, for a total of " + str(stats.get_points()) + " points.")


get_player_stats("horvat")
get_player_stats("boucher")
get_player_stats("eriksson")