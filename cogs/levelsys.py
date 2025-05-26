import discord
from discord.ext import commands
from db import leveldb

level = []
levelling = leveldb.cluster["discord"]["levelling"]

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        stats = levelling.find_one({"id" : message.author.id})

        if stats is None:
            newUser = {"id" : message.author.id, "xp" : 100}
            levelling.insert_one(newUser)
        else:
            xp = stats["xp"] + 5
            levelling.update_one({"id" : message.author.id}, {"$set" : {"xp" : xp}})
            lvl = 0
            while True:
                if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                    break
                lvl += 1
            xp -= ((50 * (lvl ** 2)) + (50 * (lvl - 1)))
            if xp == 0:
                await message.channel.send(f"Parabéns {message.author.mention}! Você subil para o level: {lvl}!")
                for i in range(len(level)):
                    if lvl == levelnum[i]
                        await message.author.add_roles(discord.utils.get(message.author.guild.roles, name = level[i]))
                        embed = discord
        
async def setup(bot):
    await bot.add_cog(LevelSystem(bot))