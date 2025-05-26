import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Load the token from .env file
load_dotenv()
token = os.environ.get('DISCORD_TOKEN')

# Logging configuration
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

# Intents
intents = discord.Intents.all()

# Bot class with setup_hook
class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension('cogs.commands')
        await self.load_extension('cogs.levelsys')
        print("[+] Cogs successfully loaded.")

# Bot instance
bot = MyBot(command_prefix='!', intents=intents)

# Evento principal
@bot.event
async def on_ready():
    print(f'🤖 Bot is online as {bot.user}')

# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
