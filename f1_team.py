from f1_driver import Driver

class Team:
    def __init__(self, team_name : str, team_color : tuple, driver1 : Driver, driver2 : Driver, points : int) -> None:
        self.team_name = team_name
        self.team_color = team_color
        self.drivers = [driver1, driver2]
        self.points = points
        pass