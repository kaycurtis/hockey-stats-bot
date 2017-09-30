class PlayerStatistics:
    def __init__(self, name, team, games_played):
        self.name = name
        self.team = team
        self.games_played = games_played

    def get_name(self):
        return self.name

    def get_team(self):
        return self.team

    def get_games_played(self):
        return self.games_played