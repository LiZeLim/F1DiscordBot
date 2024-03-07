from urllib.request import urlopen
import bs4 as bs
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import re

from f1_settings import *
from f1_team import Team

""" Formula 1 Current Season Results"""

def url_to_soup_lxml(url : str) -> BeautifulSoup:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, features = "lxml")

def setup():
    #Creating Teams and Drivers
    f1_teams_soup = url_to_soup_lxml(TEAMS_URL)
    teams = create_teams(f1_teams_soup)
    

def create_teams(f1_teams_soup : BeautifulSoup) -> list:
    f1_teams_soup_list = f1_teams_soup.find_all(class_ = "listing-link")
    f1_team_soup_list_pts = f1_teams_soup.findAll(class_ = "f1-wide--s")

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
    # Reading from the site
    race_results_soup = url_to_soup_lxml(CURR_SEASON_URL)

    # finding the results table from the html webpage
    race_results = race_results_soup.find_all('table')[0]
    race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]
    print(list(race_df.columns.values))

    #dropping useless columns
    race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis = 1)
    print(race_df.head())

if __name__ == "__main__":
    setup()
    curr_season_results()