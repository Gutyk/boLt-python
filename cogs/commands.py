from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import aiohttp

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tester_role = "tester"
        load_dotenv()
        self.weather_key = os.environ.get('WEATHER_KEY')

    # Error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, você não tem permissão para usar esse comando.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Por favor, insira um número válido.")
        else:
            await ctx.send("Ocorreu um erro ao executar o comando.")
            raise error

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
        role = discord.utils.get(ctx.guild.roles, name=self.tester_role)
        if not role:
            await ctx.send(f"Cargo '{self.test_role}' não encontrado.")
            
        if role in ctx.author.roles:
            await ctx.send(f"{ctx.author.mention} ja possui o cargo {role.name}!")

        else:
            await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention} recebeu o cargo {role.name}!")

    # Remove role from user
    @commands.command()
    async def remove(self, ctx):
        role = discord.utils.get(ctx.author.roles, name=self.tester_role)
        if role is not None:
                await ctx.author.remove_roles(role)
                await ctx.send(f"{role.name.capitalize()} removido de {ctx.author.mention}!")
        else:
            await ctx.send(f"{ctx.author.mention}, você não possui o cargo {self.tester_role}.")
    
    @commands.command()
    async def bolt(self, ctx):
        embed = discord.Embed(
            title="World Record",
            url="https://pbs.twimg.com/media/CoibgcJW8AAN-VA?format=jpg&name=4096x4096",
            description="Look at the time 9.58 SMASHING THE WORLD RECORD!",
            color=discord.Color.blue()
        )
    
    # Clear messages
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int = 1):
        if amount < 1:
            await ctx.send("Por favor, insira um número maior que zero.")
            return
        if amount > 15:
            await ctx.send("Você só pode apagar até 15 mensagens por vez.")
            return
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit=amount)
        confirmation = await ctx.send(f"Apaguei {len(deleted)} mensagens.")
        await confirmation.delete(delay=3)

    # Spam messages for testing
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, *, message="Spam!"):
        for _ in range(10):
            await ctx.send(message)
    
    # See the weather 
    @commands.command()
    async def weather(self, ctx, *, city: str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_key}&lang=pt_br&units=metric"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("Cidade não encontrada ou erro na API.")
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
    