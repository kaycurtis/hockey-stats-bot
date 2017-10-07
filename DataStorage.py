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

    # returns a list of skater stats and goalie stats matching the given name
    def parse_skater_stats(self, name):
        soup = BeautifulSoup(self.html, "html.parser")
        skater_table = soup.find(id="skater-table")
        goalie_table = soup.find(id="goalie-table")
        skater_result = self.search_table(skater_table, "skater", name)
        goalie_result = self.search_table(goalie_table, "goalie", name)
        return skater_result + goalie_result

    # takes in a table, what kind of stats are in the table, and the name of the player we are searching for
    # returns a list of player statistics or None
    def search_table(self,table,type,name):
        table_rows = table.select("tbody tr")
        matches = self.check_rows_for_player(table_rows, name)
        if matches and type == "skater":
            return self.get_skater_stats(matches)
        elif matches and type == "goalie":
            return self.get_goalie_stats(matches)
        else:
            return None

    # takes in a list of rows and returns a list of skater statistics objects corresponding to those rows
    def get_skater_stats(self, rows):
        stats = []
        for row in rows:
            player_link = rows.select("a")[0]["href"]
            match = re.match("/player/(\w+)-.*", player_link)
            first_name = match.group(1)

            match2 = re.match(".*-(\w+)-.*", player_link)
            last_name = match2.group(1)

            name = first_name + " " + last_name
            name = name.title()

            cells = rows.select("td span")[3:]

            games_played = int(cells[0].get_text())
            goals = int(cells[1].get_text())
            assists = int(cells[2].get_text())

            statistics = SkaterStatistics.SkaterStatistics(name, "Vancouver Canucks", games_played, goals, assists)
            self.player_statistics[last_name] = statistics
            stats.append(statistics)

        return stats

    # takes in a list of rows and returns a list of goalie statistics objects corresponding to those rows
    def get_goalie_stats(self, rows):
        stats = []
        for row in rows:
            player_link = rows.select("a")[0]["href"]
            match = re.match("/player/(\w+)-.*", player_link)
            first_name = match.group(1)

            match2 = re.match(".*-(\w+)-.*", player_link)
            last_name = match2.group(1)

            name = first_name + " " + last_name
            name = name.title()

            cells = rows.select("td span")[3:]
            games_played = int(cells[0].get_text())
            gaa = float(cells[8].get_text())
            save_percentage = float(cells[10].get_text())
            statistics = GoalieStatistics.GoalieStatistics(name,"Vancouver Canucks",games_played,save_percentage,gaa)
            self.player_statistics[last_name] = statistics
            stats.append(statistics)
        return stats

    # takes in a list of rows (of player data) and the name of the player we are searching for
    # returns a list of matches or None if not found
    def check_rows_for_player(self, rows, name):
        matches = []
        for row in rows:
            player_link = row.select("a")[0]["href"]
            matchObj = re.match(r".*" + name + ".*", player_link)
            if matchObj:
                matches.append(row)
        return None