import discord
import os
from discord import app_commands
import requests
import json
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('GIPHY_TOKEN')
main_guild = os.getenv('MAIN_GUILD')

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
                    await channel.send('Bot Activated..')
                    await channel.send(file=discord.File('the_grinch_intro.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     if message.content == 'ginch':
#         channel = message.channel
#         for i in range(5):
#             await channel.send('Ginch')

#     print(f'Message from {message.author}: {message.content}')
#     await bot.process_commands(message)

#     if message.content.startswith('?gif'):
#         query = message.content.split('?gif ', 1)[1]
#         gif_url = get_gif(query)
#         await message.channel.send(gif_url)

client = MyClient()

@client.tree.command(name="gif", description="Get a gif", guild=discord.Object(id=main_guild))
async def slash_command(interaction: discord.Interaction, query: str):
    response = requests.get('https://api.giphy.com/v1/gifs/translate', params={'api_key': giphy_token, 's': query})
    data = json.loads(response.text)
    gif_url = data['data']['images']['original']['url']
    await interaction.response.send_message(gif_url)

@client.tree.command(name="test", description="Test command", guild=discord.Object(id=main_guild))
async def slash_command(interaction: discord.Interaction):    
    await interaction.response.send_message("Test command executed in index.py")

client.run(discord_token)