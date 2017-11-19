#TODO so it turns out python doesn't really use getters & setters. Come back and fix this.
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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.team == other.team and self.games_played == other.games_played
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 31*(31*self.games_played + hash(self.name)) + hash(self.team)