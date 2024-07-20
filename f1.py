import numpy as np
from f1_settings import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from io import StringIO
import datetime

class F1:
    def __init__(self) -> None:
        pass

    def url_to_soup_lxml(self, url: str) -> BeautifulSoup:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        return BeautifulSoup(html, features="lxml")

    def curr_season_results(self) -> str:
        print("Current Season Results")

        # Reading from the site
        race_results_soup = self.url_to_soup_lxml(
            SEASON_URL.format(datetime.datetime.now().year)
        )

        # finding the results table from the html webpage
        race_results = race_results_soup.find_all("table")[0]
        race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]

        # dropping useless columns
        race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis=1)
        return race_df.to_markdown()

    """ 
    Currently Discord has a message character limit, therefore we can split into 2 messages:
    First message for the 1st half of the season
    Second message for the 2nd half of the season
    """

    def prev_season_result(
        self,
        year: int,
    ) -> tuple:  # tuple of str first half of season, str second half of season
        race_results_soup = self.url_to_soup_lxml(SEASON_URL.format(year))
        # print("URL", SEASON_URL.format(year))
        race_results = race_results_soup.find_all("table")[0]
        race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]

        if race_df.empty:
            print("Not a valid year")
            return

        race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis=1)

        first_half_season_df, second_half_season_df = np.array_split(race_df, 2)

        print(f"Race Results of {year}")
        return first_half_season_df.to_markdown(), second_half_season_df.to_markdown()

    def get_drivers_first_name(self) -> list[str]:
        drivers_soup = self.url_to_soup_lxml(DRIVERS_URL)
        drivers_soup_list_first_name = drivers_soup.find_all(
            class_=DRIVER_FIRST_NAME_CLASS
        )
        ls = []
        for d in drivers_soup_list_first_name:
            ls.append(d.string)
        return ls

    def get_drivers_last_name(self) -> list[str]:
        drivers_soup = self.url_to_soup_lxml(DRIVERS_URL)
        drivers_soup_list_last_name = drivers_soup.find_all(
            class_=DRIVER_LAST_NAME_CLASS
        )
        ls = []
        for d in drivers_soup_list_last_name:
            ls.append(d.string)
        return ls

    def get_drivers_pts(self) -> list[str]:
        drivers_soup = self.url_to_soup_lxml(DRIVERS_URL)
        drivers_soup_list_pts = drivers_soup.find_all(class_=DRIVER_PTS_CLASS)
        ls = []
        for p in drivers_soup_list_pts:
            ls.append(p.string)
        return ls

    def get_drivers_team(self) -> list[str]:
        drivers_soup = self.url_to_soup_lxml(DRIVERS_URL)
        drivers_soup_list_team = drivers_soup.find_all(class_=DRIVER_TEAM_CLASS)
        ls = []
        for t in drivers_soup_list_team:
            ls.append(t.string)
        return ls

    def driver_standings(self) -> str:
        drivers_first_name = self.get_drivers_first_name()
        drivers_last_name = self.get_drivers_last_name()
        drivers_pts = self.get_drivers_pts()
        drivers_team = self.get_drivers_team()

        drivers_df = pd.DataFrame(
            list(zip(drivers_first_name, drivers_last_name, drivers_pts, drivers_team)),
            columns=["First name", "Last name", "PTS", "Team"],
        )
        drivers_df["PTS"] = drivers_df["PTS"].astype(int)

        drivers_df_sorted = drivers_df.sort_values(by="PTS", ascending=False)

        print("Current Driver Standings")
        return drivers_df_sorted.to_markdown()

    def get_constructor_name(self) -> list[str]:
        team_soup = self.url_to_soup_lxml(TEAMS_URL)
        constructors_soup_list = team_soup.find_all(class_=CONSTRUCTOR_NAME_CLASS)
        ls = []
        for n in constructors_soup_list:
            ls.append(n.string)
        return ls

    def get_constructor_pts(self) -> list[str]:
        team_soup = self.url_to_soup_lxml(TEAMS_URL)
        constructor_soup_list = team_soup.find_all(class_=CONSTRUCTOR_PTS_CLASS)
        ls = []
        for p in constructor_soup_list:
            ls.append(p.string)
        return ls

    def constructors_standings(self) -> str:
        constructors_names = self.get_constructor_name()
        constructors_pts = self.get_constructor_pts()

        constructors_df = pd.DataFrame(
            list(zip(constructors_names, constructors_pts)), 
            columns=["Team", "PTS"]
        )

        constructors_df["PTS"] = constructors_df["PTS"].astype(int)

        constructors_df_sorted = constructors_df.sort_values(
            by="PTS", ascending=False
        )

        print("Current Constructors Standings")
        return constructors_df_sorted.to_markdown()
