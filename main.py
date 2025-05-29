import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
from db.tasksdb import TasksDB
import os


load_dotenv()
token = os.environ.get('DISCORD_TOKEN')

# Logging configuration
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.DEBUG, handlers=[handler])

# Intents
intents = discord.Intents.all()


class MyBot(commands.Bot):
    async def setup_hook(self):
        await TasksDB.init_db()
        await self.load_extension('cogs.commands')
        await self.load_extension('cogs.tasks')
        await self.load_extension('cogs.levelsys')
        #await self.load_extension('cogs.scheduler')
        
        print("[+] All specified cogs successfully loaded.")
        print("[+] Bot is ready to receive commands.")


bot = MyBot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot is online as {bot.user}')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
