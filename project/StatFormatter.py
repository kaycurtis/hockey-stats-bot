from project.PlayerStatsData import SkaterStatistics, GoalieStatistics

def print_stats(list_of_stats):
    result = ""
    if not list_of_stats:
        result = "It looks like you were trying to summon me, but I couldn't process your comment. You can summon me with the word !stats, followed by the first or last names of the player(s) you'd like to know about."
    for stat in list_of_stats:
        result += (print_player_stat(stat) + "\n\n")
    return result + footer()

def print_player_stat(stat):
    if isinstance(stat, SkaterStatistics.SkaterStatistics):
        return (stat.name + " has scored " + str(stat.goals) + " goals and " + str(stat.assists) + " assists in "
                + str(stat.games_played) + " games for the " + stat.team + " this year, for a total of " + str(stat.points)
                + " points. Adjusted to 82 games played, that would be " + "{0:.1f}".format(stat.goals_adjusted) + " goals and " +
                "{0:.1f}".format(stat.assists_adjusted) + " assists, for a " + "{0:.1f}".format(stat.points_adjusted) + " point season.")

    elif isinstance(stat, GoalieStatistics.GoalieStatistics):
        return stat.get_name() + " has played " + str(stat.get_games_played()) + " games this year for the " + stat.get_team() + \
               ", with a goals against average of " + str(stat.get_gaa()) + " and a " + str(stat.get_save_percentage()) + " save percentage."

def footer():
    return "\n\n^Beep ^boop ^I'm ^a ^bot. ^Check ^me ^out ^on ^[github](https://github.com/kaycurtis/hockey-stats-bot). ^Spot ^a ^bug? ^Message ^my ^mom, ^/u/go_canucks"