from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re
from tabulate import tabulate
from datetime import datetime
import datetime
import asyncio

#URLS
TEAMS_URL = "https://www.formula1.com/en/teams.html"
SEASON_URL = "https://www.formula1.com/en/results.html/{}/races.html"
DRIVERS_URL = "https://www.formula1.com/en/drivers.html"

#HTML classes
TEAMS_LISTING_CLASS = "listing-link"
TEAMS_PTS_CLASS = "f1-wide--s"

DRIVER_FIRST_NAME_CLASS = "d-block f1--xxs f1-color--carbonBlack"
DRIVER_LAST_NAME_CLASS = "d-block f1-bold--s f1-color--carbonBlack"
DRIVER_PTS_CLASS = "f1-wide--s"
DRIVER_TEAM_CLASS = "listing-item--team f1--xxs f1-color--gray5"

#Regex Patterns
NAME_PATTERN = r'\"path": ".+\"'
NAME_PATTERN_STRIP_STR = '"path: '

HREF_PATTERN = r'href=\"[^\"]+\"'
HREF_PATTERN_STRIP_STR = '"href='

COLOR_PATTERN = r'#.+\"'
COLOR_PATTERN_STRIP_STR = '"'

PTS_PATTERN = r'<div class=".*?">(.*?)<\/div>'

DRIVER_FIRST_NAME_PATTERN = r'<span class=\"d-block f1--xxs f1-color--carbonBlack\">(.+)<\/span>'
DRIVER_LAST_NAME_PATTERN = r'<span class=\"d-block f1-bold--s f1-color--carbonBlack\">(.+)<\/span>'
DRIVER_PTS_PATTERN = r'<div class="f1-wide--s">(.+)<\/div>'
DRIVER_TEAM_PATTERN = r'<p class="listing-item--team f1--xxs f1-color--gray5">(.+)<\/p>'