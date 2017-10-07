from PlayerStatsData.PlayerStatistics import PlayerStatistics

class GoalieStatistics(PlayerStatistics):
    def __init__(self,name,team,games_played,save_percentage,gaa):
        super().__init__(name,team,games_played)
        self.save_percentage = save_percentage
        self.gaa = gaa

    def get_save_percentage(self):
        return self.save_percentage

    def get_gaa(self):
        return self.gaa

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.save_percentage == other.save_percentage and self.gaa == other.gaa and super.__eq__(self,other))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)