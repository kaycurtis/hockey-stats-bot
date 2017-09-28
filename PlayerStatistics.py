class PlayerStatistics:
    def __init__(self, name, team, games_played, goals, assists):
        self.name = name
        self.team = team
        self.games_played = games_played
        self.goals = goals
        self.assists = assists
        self.points = goals + assists

    def get_name(self):
        return self.name

    def get_team(self):
        return self.team

    def get_games_played(self):
        return self.games_played

    def get_goals(self):
        return self.goals

    def get_assists(self):
        return self.assists

    def get_points(self):
        return self.points
