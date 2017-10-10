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
            return (self.goals == other.goals and self.assists == other.assists and self.name == other.name and
            self.team == other.team and self.games_played == other.games_played)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return ((self.points*31 + self.assists)*31 + self.games_played)*31 + 31*(31*self.games_played + hash(self.name)) + hash(self.team)

