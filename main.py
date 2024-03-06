from urllib.request import urlopen
import bs4 as bs
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from io import StringIO

""" Formula 1 """

# Reading from the site
url_race_results = "https://www.formula1.com/en/results.html/2023/races.html"
page = urlopen(url_race_results)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, features= "lxml")

# finding the results table from the html webpage
race_results = soup.find_all('table')[0]
race_pd = pd.read_html(StringIO(str(race_results)), header=[0])[0]
#print(list(race_pd.columns.values))

#droping useless columns
race_pd = race_pd.drop(["Unnamed: 0", "Unnamed: 7"], axis = 1)
#print(race_pd.head())
