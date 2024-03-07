from urllib.request import urlopen
import bs4 as bs
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

""" Formula 1 Current Season Results"""

def url_to_soup_lxml(url : str) -> BeautifulSoup:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, features = "lxml")

def setup():
    #Creating Teams and Drivers
    teams = []

    f1_teams_soup = url_to_soup_lxml("https://www.formula1.com/en/teams.html")
    for s in f1_teams_soup.find_all(class_ = "listing-link"):
        print(s)

def curr_season_results():
    # Reading from the site
    race_results_soup = url_to_soup_lxml("https://www.formula1.com/en/results.html/2024/races.html")

    # finding the results table from the html webpage
    race_results = race_results_soup.find_all('table')[0]
    race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]
    #print(list(race_df.columns.values))

    #dropping useless columns
    race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis = 1)
    print(race_df.head())

    value_counts = race_df['Winner'].value_counts()
    value_counts.plot(kind='bar')
    plt.title("Driver Wins")
    plt.xlabel("Driver")
    plt.ylabel("Races Won")
    plt.show()

if __name__ == "__main__":
    setup()
    #curr_season_results()