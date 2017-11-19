import re
import sys

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver

from project.PlayerStatsData import SkaterStatistics, GoalieStatistics
from project.Scraping import DataCache


class DataScraper:
    def __init__(self):
        self.data_cache = DataCache.DataCache(self.scrape())

    def find_stats_matching_word(self, name):
        # update the data if necessary
        if self.data_cache.is_expired():
            self.data_cache = DataCache.DataCache(self.scrape())
        soup = BeautifulSoup(self.data_cache.html, "html.parser")
        skater_table = soup.find(id="skater-table")
        goalie_table = soup.find(id="goalie-table")
        skater_result = self.search_table(skater_table, "skater", name)
        goalie_result = self.search_table(goalie_table, "goalie", name)
        return skater_result + goalie_result

    # takes in a table, what kind of stats are in the table, and the name of the player we are searching for
    # returns a list of player statistics or an empty list
    def search_table(self,table,type,name):
        table_rows = table.select("tbody tr")
        matches = self.check_rows_for_player(table_rows, name)
        if matches and type == "skater":
            return self.get_skater_stats(matches)
        elif matches and type == "goalie":
            return self.get_goalie_stats(matches)
        else:
            return []

    # takes in a list of rows and returns a list of skater statistics objects corresponding to those rows
    # if web scraping breaks, check here first
    def get_skater_stats(self, rows):
        stats = []
        for row in rows:
            name = self.get_player_name(row)
            cells = row.select("td span")[3:]
            games_played = int(cells[0].get_text())
            goals = int(cells[1].get_text())
            assists = int(cells[2].get_text())

            statistics = SkaterStatistics.SkaterStatistics(name, "Vancouver Canucks", games_played, goals, assists)
            self.data_cache.player_statistics[name] = statistics
            stats.append(statistics)

        return stats

    # takes in a list of rows and returns a list of goalie statistics objects corresponding to those rows
    # if web scraping breaks, check here first
    def get_goalie_stats(self, rows):
        stats = []
        for row in rows:
            name = self.get_player_name(row)
            cells = row.select("td span")[3:]
            games_played = int(cells[0].get_text())
            gaa = float(cells[8].get_text())
            save_percentage = float(cells[10].get_text())
            statistics = GoalieStatistics.GoalieStatistics(name, "Vancouver Canucks", games_played, save_percentage, gaa)
            self.data_cache.player_statistics[name] = statistics
            stats.append(statistics)
        return stats

    # From a list of rows, find those that match the name we're searching for
    def check_rows_for_player(self, rows, name):
        matches = []
        for row in rows:
            player_link = row.select("a")[0]["href"]
            matchObj = re.match(r".*/" + name + "-.*", player_link) # try to match first name
            if not matchObj:
                matchObj = re.match(r".*-" + name + "-.*", player_link)  # try to match last name
            if matchObj:
                matches.append(row)
        return matches

    # Another method that's very fragile to changes to the NHL site *shrug*
    def get_player_name(self, row):
        player_link = row.select("a")[0]["href"]    # sample: "/player/brock-boeser-8478444"

        match = re.match("/player/(\w+)-.*", player_link)
        first_name = match.group(1)

        match2 = re.match(".*-(\w+)-.*", player_link)
        last_name = match2.group(1)

        name = first_name + " " + last_name
        name = name.title()
        return name

    # Ugly switch on the platform is to make this work both on my machine & on digital ocean; TODO set up something that works with both
    def scrape(self):
        os = sys.platform
        if os == "linux":
            display = Display(visible=0, size=(800, 600))
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
        return html
