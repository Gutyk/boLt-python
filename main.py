import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.environ.get('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def greet(ctx):
    await ctx.send("POOOOOOORRAAN!")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Opa {ctx.author.mention}!")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)