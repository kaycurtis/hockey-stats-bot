from PlayerStatsData import GoalieStatistics

from project.PlayerStatsData import SkaterStatistics


def print_stats(list_of_stats):
    result = ""
    for stat in list_of_stats:
        result += (print_player_stat(stat) + "\n")
    return result

def print_player_stat(stat):
    if isinstance(stat, SkaterStatistics.SkaterStatistics):
        return (stat.get_name() + " has scored " + str(stat.get_goals()) + " goals and " + str(stat.get_assists()) + " assists in "
                + str(stat.get_games_played()) + " games for the " + stat.get_team() + " this year, for a total of " + str(stat.get_points())
                + " points." + footer())
    elif isinstance(stat, GoalieStatistics.GoalieStatistics):
        return stat.get_name() + " has played " + str(stat.get_games_played()) + " games this year for the " + stat.get_team() + \
               ", with a goals against average of " + str(stat.get_gaa()) + " and a " + str(stat.get_save_percentage()) + " save percentage." + footer()

def footer():
    return "\n\n^Beep boop I'm a bot. Check me out on [github](https://github.com/kaycurtis/hockey-stats-bot). Spot a bug? Message my mom, /u/go_canucks"