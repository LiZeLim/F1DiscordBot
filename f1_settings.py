TEAMS_URL = "https://www.formula1.com/en/teams.html"
CURR_SEASON_URL = "https://www.formula1.com/en/results.html/2024/races.html"

NAME_PATTERN = r'\"path": ".+\"'
NAME_PATTERN_STRIP_STR = '"path: '

HREF_PATTERN = r'href=\"[^\"]+\"'
HREF_PATTERN_STRIP_STR = '"href='

COLOR_PATTERN = r'#.+\"'
COLOR_PATTERN_STRIP_STR = '"'

PTS_PATTERN = r'<div class=".*?">(.*?)<\/div>'