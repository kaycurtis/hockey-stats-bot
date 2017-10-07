from PlayerStatsData.PlayerStatistics import PlayerStatistics

class SkaterStatistics(PlayerStatistics):
    def __init__(self, name, team, games_played, goals, assists):
        super().__init__(name, team, games_played)
        self.goals = goals
        self.assists = assists
        self.points = goals + assists

    def get_goals(self):
        return self.goals

    def get_assists(self):
        return self.assists

    def get_points(self):
        return self.points

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
            self.goals == other.goals and self.assists == other.assists and super.__eq__(self, other))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)