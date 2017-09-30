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
