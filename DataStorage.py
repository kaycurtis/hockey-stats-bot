import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import datetime
import PlayerStatistics

class DataCache:
    def __init__(self, html):
        self.date_created = datetime.datetime.now()
        self.html = html
        self.player_statistics = {}

    def is_expired(self):
        date = datetime.datetime.now()
        if date.date() != self.date_created.date():
            return True
        else:
            return False

    def get_player_stats(self, name):
        if self.player_statistics.get(name) is None:
            return self.parse_player_stats(name)
        else:
            return self.player_statistics.get(name)

    def parse_player_stats(self,name):
        soup = BeautifulSoup(self.html, "html.parser")

        container = soup.find(class_="stats__content")
        table_rows = container.select("tbody tr")

        row_with_player = self.check_rows_for_player(table_rows, name)

        if row_with_player:
            return self.get_stats(row_with_player)

    def get_stats(self,row):
        player_link = row.select("a")[0]["href"]
        match = re.match("/player/(\w+)-.*", player_link)
        first_name = match.group(1)

        match2 = re.match(".*-(\w+)-.*", player_link)
        last_name = match2.group(1)

        name = first_name + " " + last_name
        name = name.title()

        cells = row.select("td span")

        games_played = int(cells[3].get_text())
        goals = int(cells[4].get_text())
        assists = int(cells[5].get_text())

        statistics = PlayerStatistics.PlayerStatistics(name, "Vancouver Canucks", games_played, goals, assists)
        self.player_statistics[last_name] = statistics
        return statistics

    def check_rows_for_player(self,rows, name):
        for row in rows:
            player_link = row.select("a")[0]["href"]
            matchObj = re.match(r".*" + name + ".*", player_link)
            if matchObj:
                return row
        return False