from f1_driver import Driver

class Team:
    def __init__(self, team_name : str, team_color : str, points : int) -> None:
        self.team_name = team_name
        self.team_color = team_color
        self.points = points

        self.drivers = [] #Drivers object
        pass

    def add_driver(self, driver : Driver) -> None:
        self.drivers.append(driver)
        pass