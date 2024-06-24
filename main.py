import numpy as np
from dotenv import load_dotenv
import os
import discord
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import re
from tabulate import tabulate
import datetime
import asyncio

from f1 import F1

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # TODO Make a user guide for the discord bot containing the possible commands, etc
    if message.content.startswith("!F1") or message.content.startswith("!f1"):
        pass

    elif message.content.startswith("!Season") or message.content.startswith("!season"):
        await message.channel.send("```" + f.curr_season_results() + "```")

    elif message.content.startswith("!Drivers") or message.content.startswith(
        "!drivers"
    ):
        await message.channel.send("```" + f.driver_standings() + "```")

    elif message.content.startswith("!Constructors") or message.content.startswith(
        "!constructors"
    ):
        await message.channel.send("```" + f.constructors_standings() + "```")

    elif message.content.startswith("!PrevSeason") or message.content.startswith(
        "!prevSeason"
    ):
        channel = message.channel

        await message.channel.send("Please enter year")

        """ Message checking validity of the message, given that it can be numeric and that we able to retrieve that year """

        def check(year: str) -> bool:
            return year.channel == channel

        try:
            year = await client.wait_for("message", timeout=10, check=check)

            if not year.content.isnumeric():
                await message.channel.send(
                    "Please enter a valid year in the format of YYYY"
                )
                return

            year = int(year.content)
            curr_year = int(datetime.date.today().strftime("%Y"))

            if year < 1950 or year > curr_year:
                await message.channel.send(
                    f"Invalid Year, please enter a year from 1950 till {curr_year}"
                )
                return

        except asyncio.TimeoutError:
            await channel.send("Timeout")
        else:
            first_half_markdown, second_half_markdown = f.prev_season_result(year)
            await message.channel.send(
                "1st half of season\n" + "```" + first_half_markdown + "```"
            )
            await message.channel.send(
                "2nd half of season\n" + "```" + second_half_markdown + "```"
            )


if __name__ == "__main__":
    f = F1()
    client.run(TOKEN)
