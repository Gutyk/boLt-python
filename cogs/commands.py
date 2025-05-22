from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import aiohttp

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_role = "teste"
        load_dotenv()
        self.weather_key = os.environ.get('WEATHER_KEY')


    # Command to verify if the bot is running
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Opa {ctx.author.mention}!")

    # Check bot's latency
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round (self.bot.latency * 1000)}ms!")

    # Assign role to user
    @commands.command()
    async def assign(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name=self.test_role)
        if not role:
            await ctx.send(f"Cargo '{self.test_role}' não encontrado.")
            
        if role in ctx.author.roles:
            await ctx.send(f"{ctx.author.mention} ja possui o cargo {role.name}!")

        else:
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention} recebeu o cargo {role.name}!")

    # See the weather 
    @commands.command()
    async def weather(self, ctx, *, city: str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_key}&lang=pt_br&units=metric"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("❌ Cidade não encontrada ou erro na API.")
                    return

                dados = await response.json()

                nome = dados["name"]
                clima = dados["weather"][0]["description"].capitalize()
                temp = dados["main"]["temp"]
                sensacao = dados["main"]["feels_like"]
                umidade = dados["main"]["humidity"]

                if 28 < temp:
                    color = discord.Color.red()
                elif 24 < temp <= 28:
                    color = discord.Color.orange()
                elif 20 < temp <= 24:
                    color = discord.Color.yellow()
                elif 10 < temp <= 20:
                    color = discord.Color.dark_blue()
                else:
                    color = discord.Color.blue

                embed = discord.Embed(
                    title=f"☁️ Clima em {nome}",
                    color = color
                )
                embed.add_field(name="Temperatura", value=f"{round(temp)}°C", inline=True)
                embed.add_field(name="Sensação", value=f"{round(sensacao)}°C", inline=True)
                embed.add_field(name="Umidade", value=f"{umidade}%", inline=True)
                embed.add_field(name="Condição", value=clima, inline=False)

                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))
    