import discord
from discord.ext import commands
#rom db import tasksdb
from dotenv import load_dotenv
import os

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.channel_id = os.environ.get('CHANNEL_ID')

    @commands.command(name="addtask")
    async def add_task(self, ctx, *, task: str):
        #tasksdb.add_task(ctx.author.id, task)
        await ctx.send(f"✅ Tarefa adicionada: **{task}**")

    # @commands.command(name="tasks")
    # async def list_tasks(self, ctx):
    #     tasks = tasksdb.get_pending_tasks(ctx.author.id)
    #     if tasks:
    #         description = "\n".join([f"{idx+1}. {t['task']}" for idx, t in enumerate(tasks)])
    #         embed = discord.Embed(title="📋 Tarefas Pendentes", description=description, color=discord.Color.green())
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send("🎉 Você não tem tarefas pendentes!")

    # @commands.command(name="donetask")
    # async def done_task(self, ctx, task_number: int):
    #     tasks = tasksdb.get_pending_tasks(ctx.author.id)
    #     if 0 < task_number <= len(tasks):
    #         tasksdb.complete_task(ctx.author.id, task_number - 1)
    #         await ctx.send(f"✅ Tarefa concluída: **{tasks[task_number - 1]['task']}**")
    #     else:
    #         await ctx.send("⚠️ Número inválido de tarefa.")

async def setup(bot):
    await bot.add_cog(Tasks(bot))