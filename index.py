import discord
from discord import app_commands
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('GIPHY_TOKEN')
main_guild = os.getenv('MAIN_GUILD')


async def get_gif(query):
    response = requests.get('https://api.giphy.com/v1/gifs/translate', params={'api_key': giphy_token, 's': query})
    data = json.loads(response.text)
    gif_url = data['data']['images']['original']['url']
    return gif_url


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
    
    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=main_guild))
        print(f'Logged in as {self.user}')
        await self.send_intro()

    async def send_intro(self):
        for guild in self.guilds:
            for channel in guild.text_channels:
                if str(channel) == "general":
                    await channel.send('*** The Ginch Has Arrived ***')
                    await channel.send(file=discord.File('the_grinch_intro.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))


client = MyClient()


@client.tree.command(name="gif", description="Get a gif", guild=discord.Object(id=main_guild))
async def slash_command(interaction: discord.Interaction, query: str):
    try:
        gif_url = await get_gif(query)
        await interaction.response.send_message(gif_url)
    except:
        await interaction.response.send_message('No gif found')

@client.tree.command(name="ginch", description="Summon the ginch", guild=discord.Object(id=main_guild))
async def slash_command(interaction: discord.Interaction, query: str):
    if query == 'ginch':
        channel = interaction.channel
        try:
            for i in range(5):
                await channel.send('*** I have been summoned ***')
        except:
            await interaction.response.send_message('*** Error summoning the ginch ***')


client.run(discord_token)