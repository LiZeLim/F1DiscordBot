from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re
from tabulate import tabulate
from datetime import datetime

from f1_settings import *
from f1_team import Team
from f1_driver import Driver

def url_to_soup_lxml(url : str) -> BeautifulSoup:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, features = "lxml")

def setup() -> tuple:
    #Creating Teams and Drivers
    teams = create_teams()
    drivers = create_drivers(teams)

    return teams, drivers
    
def create_drivers(teams : list[Team]) -> None:
    drivers_soup = url_to_soup_lxml(DRIVERS_URL)

    drivers_soup_list_first_name = drivers_soup.find_all(class_ = DRIVER_FIRST_NAME_CLASS)
    drivers_soup_list_last_name = drivers_soup.find_all(class_ = DRIVER_LAST_NAME_CLASS)
    drivers_soup_list_pts = drivers_soup.find_all(class_ = DRIVER_PTS_CLASS)
    drivers_soup_list_team = drivers_soup.find_all(class_ = DRIVER_TEAM_CLASS)
    
    drivers = []

    for index in range(0, len(drivers_soup_list_first_name)):
        first_name = re.findall(DRIVER_FIRST_NAME_PATTERN, str(drivers_soup_list_first_name[index]).strip())[0]
        last_name = re.findall(DRIVER_LAST_NAME_PATTERN, str(drivers_soup_list_last_name[index]).strip())[0]
        pts = re.findall(DRIVER_PTS_PATTERN, str(drivers_soup_list_pts[index]).strip())[0]
        drivers_team = re.findall(DRIVER_TEAM_PATTERN, str(drivers_soup_list_team[index]).strip())[0]

        for team in teams:
            if (team.team_name.upper() == drivers_team.upper()):
                driver = Driver(first_name, last_name, drivers_team, pts)
                team.add_driver(driver)
                drivers.append(driver)
    return drivers

def create_teams() -> list[Team]:
    f1_teams_soup = url_to_soup_lxml(TEAMS_URL)
    f1_teams_soup_list = f1_teams_soup.find_all(class_ = TEAMS_LISTING_CLASS)
    f1_team_soup_list_pts = f1_teams_soup.findAll(class_ = TEAMS_PTS_CLASS)

    teams = []

    points_ls = []
    for p in f1_team_soup_list_pts:
        p_str = str(p).strip()
        extract = re.findall(PTS_PATTERN, p_str)
        points_ls.append(int(extract[0]))

    points_ls_index = 0

    for f in f1_teams_soup_list:
        soup_str = str(f).strip()

        team_name = extract_team_details(soup_str, NAME_PATTERN, NAME_PATTERN_STRIP_STR)
        team_color = extract_team_details(soup_str, COLOR_PATTERN, COLOR_PATTERN_STRIP_STR)
        team_pts = points_ls[points_ls_index]

        # TODO team_href = extract_team_details(soup_str, HREF_PATTERN, HREF_PATTERN_STRIP_STR)

        teams.append(Team(team_name, team_color, team_pts))

        points_ls_index += 1
    
    return teams

def extract_team_details(soup_str : str, regex_extraction_pattern : str, strip_pattern : str) -> str:
    extract = re.findall(regex_extraction_pattern, soup_str)[0]
    return extract.strip(strip_pattern)

def curr_season_results() -> None:
    print("Current Season Results")

    # Reading from the site
    race_results_soup = url_to_soup_lxml(SEASON_URL.format(datetime.now().year))

    # finding the results table from the html webpage
    race_results = race_results_soup.find_all('table')[0]
    race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]

    #dropping useless columns
    race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis = 1)
    print(race_df.to_markdown())

def prev_season_result(year : int) -> None:
    race_results_soup = url_to_soup_lxml(SEASON_URL.format(year))
    race_results = race_results_soup.find_all('table')[0]
    race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]

    if race_df.empty:
        print("Not a valid year")
        return

    race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis = 1)
    print(f"Race Results of {year}")
    print(race_df.to_markdown())
    

def driver_standings(drivers : list[Driver]) -> None:
    drivers_df = pd.DataFrame([driver.__dict__ for driver in drivers])
    drivers_df['pts'] = drivers_df['pts'].astype(int)

    drivers_df_sorted = drivers_df.sort_values(by="pts", ascending = False)

    print("Current Driver Standings")
    print(drivers_df_sorted.to_markdown())
    pass

def constructors_standings(teams : list[Team]) -> None:
    constructors_df = pd.DataFrame([team.__dict__ for team in teams])
    constructors_df = constructors_df.drop(["team_color", "drivers"], axis = 1)

    constructors_df["points"] = constructors_df["points"].astype(int)

    constructors_df_sorted = constructors_df.sort_values(by="points", ascending = False)

    print("Current Constructors Standings")
    print(constructors_df_sorted.to_markdown())
    pass

if __name__ == "__main__":
    teams, drivers = setup()

    curr_season_results()
    driver_standings(drivers)
    constructors_standings(teams)
    prev_season_result(2023)