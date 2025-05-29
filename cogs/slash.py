from discord.ext import commands
from discord import app_commands
import discord

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="teste", description="Comando de teste")
    async def teste(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Olá, {interaction.user.mention}!")

async def setup(bot: commands.Bot):
    await bot.add_cog(SlashCommands(bot))
