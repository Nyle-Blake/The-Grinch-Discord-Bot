import discord
import os
from discord.ext import commands
import requests
import json
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
giphy_token = os.getenv('GIPHY_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "general":
                await channel.send('Bot Activated..')
                await channel.send(file=discord.File('the_grinch_intro.gif'))
    print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))

def get_gif(query):
    response = requests.get('https://api.giphy.com/v1/gifs/translate', params={'api_key': giphy_token, 's': query})
    data = json.loads(response.text)
    gif_url = data['data']['images']['original']['url']
    return gif_url

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '?ginch':
        channel = message.channel
        for i in range(5):
            await channel.send('Ginch')

    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)

    if message.content.startswith('?gif'):
        query = message.content.split('?gif ', 1)[1]
        gif_url = get_gif(query)
        await message.channel.send(gif_url)

bot.run(discord_token)