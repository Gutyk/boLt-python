import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta
import asyncio

class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_checkin.start()  

    def cog_unload(self):
        self.daily_checkin.cancel()  
        
    def define_target_time(self, hour, minute):
        now = datetime.now()
        target_time = datetime.combine(now.date(), time(hour=hour, minute=minute))
        
        if now >= target_time:
            target_time += timedelta(days=1)
        
        return target_time
        
    @tasks.loop(hours=24)
    async def daily_tasks(self):
        channel_id = SEU_CHANNEL_ID_AQUI  
        channel = self.bot.get_channel(channel_id)
        
        embed = discord.Embed(
            title="🌞 Bom dia!",
            description="Use o comando `!addtask <sua tarefa>` para adicionar as tarefas de hoje!",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)
        
        
        
    ### implementar db e revisar comandos
        

    @daily_tasks.before_loop
    async def before_daily_tasks(self):
        await self.bot.wait_until_ready() 
        now = datetime.now()
        target_time = self.define_target_time(8, 0)
        return asyncio.sleep((target_time - now).total_seconds())  
        
        
    @tasks.loop(hours=24)
    async def daily_checkin(self):
        channel_id = SEU_CHANNEL_ID_AQUI  
        channel = self.bot.get_channel(channel_id)
        
        embed = discord.Embed(
        title="🌙 Boa noite!",
        description="Hora de revisar suas tarefas!",
        color=discord.Color.dark_purple()
    )

        guild = channel.guild
        for member in guild.members:
            if not member.bot:
                tasks = tasksdb.get_pending_tasks(member.id)
                if tasks:
                    description = "\n".join([f"{idx+1}. {t['task']}" for idx, t in enumerate(tasks)])
                    user_embed = discord.Embed(
                        title="📋 Suas tarefas pendentes hoje",
                        description=description,
                        color=discord.Color.purple()
                    )
                    await member.send(embed=user_embed)
                else:
                    await member.send("🎉 Você não tem tarefas pendentes hoje! Bom descanso.")

        await channel.send(embed=embed)
   

    @daily_checkin.before_loop
    async def before_daily_checkin(self):
        await self.bot.wait_until_ready() 
        now = datetime.now()
        target_time = self.define_target_time(20, 0)  

        await asyncio.sleep((target_time - now).total_seconds())

async def setup(bot):
    await bot.add_cog(Scheduler(bot))
