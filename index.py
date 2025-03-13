import requests
import json
from dotenv import load_dotenv
import discord
from MyClient import MyClient

load_dotenv()


async def get_gif(query, api_key):
    response = requests.get('https://api.giphy.com/v1/gifs/translate', params={'api_key': api_key, 's': query})
    data = json.loads(response.text)
    gif_url = data['data']['images']['original']['url']
    return gif_url
 
client = MyClient()


@client.tree.command(name="gif", description="Get a gif", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction, query: str):
    try:
        gif_url = await get_gif(query, client.giphy_token)
        await interaction.response.send_message(gif_url)
    except:
        await interaction.response.send_message('No gif found')

@client.tree.command(name="grinch", description="Summon the grinch", guild=discord.Object(id=client.main_guild))
async def slash_command(interaction: discord.Interaction, query: str):
    if query == 'grinch':
        channel = interaction.channel
        try:
            for i in range(5):
                await channel.send('*** I have been summoned ***')
        except:
            await interaction.response.send_message('*** Error summoning the grinch ***')
    else:
        await interaction.response.send_message('** The grinch has not been summoned **')

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