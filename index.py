import discord
import os
from dotenv import load_dotenv

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        channel = message.channel

        if message.author == self.user:
            return
        
        if message.content == '$ginch':
            channel = message.channel
            await channel.send('I am the ginch')

        if message.content == 'You are a what?':
            channel = message.channel
            for i in range(10):
                await channel.send('Ginch')
        
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('TOKEN'))