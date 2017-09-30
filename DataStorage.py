import datetime
import re

from bs4 import BeautifulSoup

from PlayerStatsData import SkaterStatistics
from PlayerStatsData import GoalieStatistics


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
            return self.parse_skater_stats(name)
        else:
            return self.player_statistics.get(name)

    def parse_skater_stats(self, name):
        soup = BeautifulSoup(self.html, "html.parser")
        skater_table = soup.find(id="skater-table")
        goalie_table = soup.find(id="goalie-table")
        skater_result = self.search_table(skater_table, "skater", name)
        if skater_result is not None:
            return skater_result
        else:
            return self.search_table(goalie_table, "goalie", name)


    def search_table(self,table,type,name):
        table_rows = table.select("tbody tr")
        row_with_player = self.check_rows_for_player(table_rows, name)
        if row_with_player and type == "skater":
            return self.get_skater_stats(row_with_player)
        elif row_with_player and type == "goalie":
            return self.get_goalie_stats(row_with_player)
        else:
            return None

    def get_skater_stats(self, row):
        player_link = row.select("a")[0]["href"]
        match = re.match("/player/(\w+)-.*", player_link)
        first_name = match.group(1)

        match2 = re.match(".*-(\w+)-.*", player_link)
        last_name = match2.group(1)

        name = first_name + " " + last_name
        name = name.title()

        cells = row.select("td span")[3:]

        games_played = int(cells[0].get_text())
        goals = int(cells[1].get_text())
        assists = int(cells[2].get_text())

        statistics = SkaterStatistics.SkaterStatistics(name, "Vancouver Canucks", games_played, goals, assists)
        self.player_statistics[last_name] = statistics
        return statistics

    def get_goalie_stats(self,row):
        player_link = row.select("a")[0]["href"]
        match = re.match("/player/(\w+)-.*", player_link)
        first_name = match.group(1)

        match2 = re.match(".*-(\w+)-.*", player_link)
        last_name = match2.group(1)

        name = first_name + " " + last_name
        name = name.title()

        cells = row.select("td span")[3:]
        games_played = int(cells[0].get_text())
        gaa = float(cells[8].get_text())
        save_percentage = float(cells[10].get_text())
        statistics = GoalieStatistics.GoalieStatistics(name,"Vancouver Canucks",games_played,save_percentage,gaa)
        self.player_statistics[last_name] = statistics
        return statistics

    def check_rows_for_player(self,rows, name):
        for row in rows:
            player_link = row.select("a")[0]["href"]
            matchObj = re.match(r".*" + name + ".*", player_link)
            if matchObj:
                return row
        return False