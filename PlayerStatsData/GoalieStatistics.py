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