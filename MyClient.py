import os
import discord
from discord import app_commands

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.giphy_token = os.getenv('GIPHY_TOKEN')
        self.main_guild = os.getenv('MAIN_GUILD')
    
    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=self.main_guild))
        print(f'Logged in as {self.user}')
        await self.send_intro()

    async def send_intro(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                if str(channel) == "general":
                    await channel.send('*** The Ginch Has Arrived ***')
                    await channel.send(file=discord.File('the_grinch_intro.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))