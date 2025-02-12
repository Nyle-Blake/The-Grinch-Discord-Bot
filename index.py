import discord
from discord import app_commands
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


async def get_gif(query, api_key):
    response = requests.get('https://api.giphy.com/v1/gifs/translate', params={'api_key': api_key, 's': query})
    data = json.loads(response.text)
    gif_url = data['data']['images']['original']['url']
    return gif_url


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


client = MyClient()


@client.tree.command(name="gif", description="Get a gif", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction, query: str):
    try:
        gif_url = await get_gif(query, client.giphy_token)
        await interaction.response.send_message(gif_url)
    except:
        await interaction.response.send_message('No gif found')

@client.tree.command(name="ginch", description="Summon the ginch", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction, query: str):
    if query == 'ginch':
        channel = interaction.channel
        try:
            for i in range(5):
                await channel.send('*** I have been summoned ***')
        except:
            await interaction.response.send_message('*** Error summoning the ginch ***')

@client.tree.command(name="kick", description="Kick a member of the server", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction, member: discord.Member, reason: str):
    try:
        if reason == '':
            await interaction.response.send_message('*** Please provide a reason ***')
            return
        await member.send(f'You have been kicked from the server.\n Reason: {reason}')
        await member.kick()
        await interaction.response.send_message(f'{member} has been kicked.\n Reason: {reason}')
    except:
        await interaction.response.send_message('*** Error kicking the member ***')

@client.tree.command(name="ban", description="Ban a member of the server", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction, member: discord.Member, reason: str):
    try:
        if reason == '':
            await interaction.response.send_message('*** Please provide a reason ***')
            return
        await member.send(f'You have been banned from the server.\n Reason: {reason}')
        await member.ban()
        await interaction.response.send_message(f'{member} has been banned.\n Reason: {reason}')
    except:
        await interaction.response.send_message('*** Error banning the member ***')

@client.tree.command(name="unban", description="Unban a member of the server", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction, member: discord.Member, reason: str):
    try:
        if reason == '':
            await interaction.response.send_message('*** Please provide a reason ***')
            return
        await member.send(f'You have been unbanned from the server.\n Reason: {reason}')
        await member.unban()
        await interaction.response.send_message(f'{member} has been unbanned.\n Reason: {reason}')
    except:
        await interaction.response.send_message('*** Error unbanning the member ***')

@client.tree.command(name="ping", description="Check the bot's latency", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction):
    try:
        latency = round(client.latency * 1000)  # Convert latency to milliseconds
        await interaction.response.send_message(f'Ping! Latency is {latency}ms')
    except:
        interaction.response.send_message('*** Error checking the latency ***')


if __name__ == '__main__':
    client.run(client.discord_token)