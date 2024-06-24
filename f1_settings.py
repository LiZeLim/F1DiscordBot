# URLS
TEAMS_URL = "https://www.formula1.com/en/teams"
SEASON_URL = "https://www.formula1.com/en/results.html/{}/races.html"
DRIVERS_URL = "https://www.formula1.com/en/drivers"

# HTML classes
TEAMS_LISTING_CLASS = "listing-link"
TEAMS_PTS_CLASS = "f1-wide--s"

# Driver classes
DRIVER_FIRST_NAME_CLASS = "f1-heading tracking-normal text-fs-12px leading-tight uppercase font-normal non-italic f1-heading__body font-formulaOne"
DRIVER_LAST_NAME_CLASS = "f1-heading tracking-normal text-fs-18px leading-tight uppercase font-bold non-italic f1-heading__body font-formulaOne"
DRIVER_PTS_CLASS = "f1-heading-wide font-formulaOneWide tracking-normal font-normal non-italic text-fs-18px leading-none normal-case"
DRIVER_TEAM_CLASS = "f1-heading tracking-normal text-fs-12px leading-tight normal-case font-normal non-italic f1-heading__body font-formulaOne text-greyDark"

# Constructor classes
CONSTRUCTOR_NAME_CLASS = "f1-heading tracking-normal text-fs-20px tablet:text-fs-25px leading-tight normal-case font-bold non-italic f1-heading__body font-formulaOne"
CONSTRUCTOR_PTS_CLASS = "f1-heading-wide font-formulaOneWide tracking-normal font-normal non-italic text-fs-18px leading-none normal-case"

# Regex Patterns
NAME_PATTERN = r'\"path": ".+\"'
NAME_PATTERN_STRIP_STR = '"path: '

HREF_PATTERN = r"href=\"[^\"]+\""
HREF_PATTERN_STRIP_STR = '"href='

COLOR_PATTERN = r"#.+\""
COLOR_PATTERN_STRIP_STR = '"'
