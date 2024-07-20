# F1 Discord Bot

Please invite the bot to your discord server first:
[**Invite bot Link**](https://discord.com/oauth2/authorize?client_id=1216315254502588467)

**Commands (all start with !):**

* !F1/f1: Latest Race Results
* !Season/season: Current Season Standings
* !Drivers/drivers: Driver Championship Standings
* !Constructors/constructors: Constructor Standings
* !PrevSeason/prevseason (Coming Soon!): Previous Season Standings

**Tip:** Use commands in any text channel for F1 updates.

## Self Run

To run the bot instance locally, you need to create a discord developer account, please create an account here: [**Discord Developer Portal**](https://discord.com/developers/docs/intro)

1. Within the Discord developer portal, select Applications (top left menu bar), then new application.
2. Name the application
3. After creating the new discord bot application, within the settings menu bar select "Bot".
4. To generate a discord bot token, under the token heading select reset token. Please save this token in a .env file.
5. Fork the repo, and create a .env file and add:
```DISCORD_TOKEN=your_discord_token```
6. Invite the bot, by generate an invite link from the Discord developer portal.
7. Within the installation settings, under Default Install Settings. Add bot under the Guild Install.
8. Add the following permissions: Read MEssage History, Read Messages/View Channels, Send Messages, and Send Messages in Threads.
9. Finally run the application using in your terminal: ```python main.py```
