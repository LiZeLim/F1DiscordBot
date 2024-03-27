from f1_settings import *
from f1_team import Team
from f1_driver import Driver

import discord

TOKEN = ""

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def url_to_soup_lxml(url : str) -> BeautifulSoup:
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, features = "lxml")

def setup() -> tuple:
    print("Setting up")

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

def curr_season_results() -> str:
    print("Current Season Results")

    # Reading from the site
    race_results_soup = url_to_soup_lxml(SEASON_URL.format(datetime.now().year))

    # finding the results table from the html webpage
    race_results = race_results_soup.find_all("table")[0]
    race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]

    #dropping useless columns
    race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis = 1)
    return race_df.to_markdown()

""" 
Currently Discord has a message character limit, therefore we can split into 2 messages:
First message for the 1st half of the season
Second message for the 2nd half of the season
 """
# TODO split results matrix into 2 sections, so that the bot can print it out into 2 different messages.
def prev_season_result(year : int) -> str:
    race_results_soup = url_to_soup_lxml(SEASON_URL.format(year))
    print("URL", SEASON_URL.format(year))
    race_results = race_results_soup.find_all("table")[0]
    race_df = pd.read_html(StringIO(str(race_results)), header=[0])[0]

    if race_df.empty:
        print("Not a valid year")
        return

    race_df = race_df.drop(["Unnamed: 0", "Unnamed: 7"], axis = 1)
    print(f"Race Results of {year}")
    return race_df.to_markdown()
    
def driver_standings(drivers : list[Driver]) -> str:
    drivers_df = pd.DataFrame([driver.__dict__ for driver in drivers])
    drivers_df["pts"] = drivers_df["pts"].astype(int)

    drivers_df_sorted = drivers_df.sort_values(by="pts", ascending = False)

    print("Current Driver Standings")
    return drivers_df_sorted.to_markdown()

def constructors_standings(teams : list[Team]) -> str:
    constructors_df = pd.DataFrame([team.__dict__ for team in teams])
    constructors_df = constructors_df.drop(["team_color", "drivers"], axis = 1)

    constructors_df["points"] = constructors_df["points"].astype(int)

    constructors_df_sorted = constructors_df.sort_values(by="points", ascending = False)

    print("Current Constructors Standings")
    return constructors_df_sorted.to_markdown()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!F1") or message.content.startswith("!f1"):
        pass

    elif message.content.startswith("!Season") or message.content.startswith("!season"):
        await message.channel.send("```" + curr_season_results() + "```")

    elif message.content.startswith("!Drivers") or message.content.startswith("!drivers"):
        await message.channel.send("```" + driver_standings(drivers) + "```")

    elif message.content.startswith("!Constructors") or message.content.startswith("!constructors"):
        await message.channel.send("```" + constructors_standings(teams) + "```")

    elif message.content.startswith("!OldConstructors") or message.content.startswith("!oldConstructors"):
        channel = message.channel
        
        """ Message checking validity of the message, given that it can be numeric and that we able to retrieve that year """
        def check(year : str) -> bool:
            return year.channel == channel

        try:
            year = await client.wait_for('message', timeout=10, check=check)

            if not year.content.isnumeric():
                await message.channel.send("Please enter a valid year in the format of YYYY")
                return

            year = int(year.content)
            curr_year = int(datetime.date.today().strftime("%Y"))

            if year < 1950 or year > curr_year:
                await message.channel.send(f"Invalid Year, please enter a year from 1950 till {curr_year}")
                return
            
        except asyncio.TimeoutError:
            await channel.send("Timeout")
        else:
            await message.channel.send("```" + prev_season_result(year) + "```")

teams, drivers = setup()

if __name__ == "__main__":
    client.run(TOKEN)
