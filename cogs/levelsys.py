import discord
from discord.ext import commands
from db import leveldb

level = ["lv5", "lv10", "lv15"]
levelnum = [5, 10, 14]

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        # Busca ou cria documento do usuário
        stats = leveldb.get_user_document(message.author.id, message.guild.id)

        xp = stats["xp"] + 5
        leveldb.update_user(message.author.id, message.guild.id, {"xp": xp})

        lvl = 0
        while True:
            if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1

        xp_needed = (50 * (lvl ** 2)) + (50 * (lvl - 1))
        xp_to_next_level = xp - xp_needed

        if xp_to_next_level == 0:
            await message.channel.send(f"Parabéns {message.author.mention}! Você subiu para o level: {lvl}!")

            for i in range(len(level)):
                if lvl == levelnum[i]:
                    role = discord.utils.get(message.guild.roles, name=level[i])
                    if role:
                        await message.author.add_roles(role)
                        embed = discord.Embed(description=f"{message.author.mention} você recebeu o cargo {level[i]}!")
                        embed.set_thumbnail(url=message.author.avatar.url)
                        await message.channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        stats = leveldb.get_user_document(ctx.author.id, ctx.guild.id)
        xp = stats["xp"]

        # Cálculo do level com base no XP total
        lvl = 0
        while True:
            if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                break
            lvl += 1

        # XP do nível anterior (nível anterior é lvl - 1)
        previous_level_xp = (50 * ((lvl - 1) ** 2)) + (50 * (lvl - 2)) if lvl > 1 else 0
        xp_in_level = xp - previous_level_xp
        next_level_xp = ((50 * (lvl ** 2)) + (50 * (lvl - 1))) - previous_level_xp

        # Barra de progresso proporcional
        progress_ratio = min(max(xp_in_level / next_level_xp, 0), 1)
        filled_boxes = int(progress_ratio * 20)
        empty_boxes = 20 - filled_boxes
        progress_bar = (":blue_square:" * filled_boxes) + (":white_large_square:" * empty_boxes)

        # Ranking geral
        ranking = list(leveldb.collection.find({"guild_id": str(ctx.guild.id)}).sort("xp", -1))
        rank = 1
        for entry in ranking:
            if entry["user_id"] == str(ctx.author.id):
                break
            rank += 1

        # Embed final
        embed = discord.Embed(
            title=f"Nível de {ctx.author.display_name}",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.add_field(name="Level", value=str(lvl), inline=True)
        embed.add_field(name="XP", value=f"{xp_in_level}/{next_level_xp}", inline=True)
        embed.add_field(name="Rank", value=f"#{rank}", inline=True)
        embed.add_field(name="Progresso", value=progress_bar, inline=False)

        await ctx.channel.send(embed=embed)


    @commands.command()
    async def leaderboard(self, ctx):
        rankings = leveldb.collection.find({"guild_id": str(ctx.guild.id)}).sort("xp", -1)

        embed = discord.Embed(
            title="🏆 Leaderboard - Top 10",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty)
        embed.set_footer(text=f"Servidor: {ctx.guild.name}")

        medalhas = ["🥇", "🥈", "🥉"]
        description = ""

        i = 1
        for user in rankings:
            if i > 10:
                break

            member = ctx.guild.get_member(int(user["user_id"]))
            if not member:
                continue

            medalha = medalhas[i - 1] if i <= 3 else f"`#{i}`"
            nome = member.display_name
            xp = user["xp"]

            description += f"{medalha} **{nome}** — `{xp} XP`\n"
            i += 1

        embed.description = description or "Ninguém foi ranqueado ainda."
        await ctx.send(embed=embed)

# Setup
async def setup(bot):
    await bot.add_cog(LevelSystem(bot))
