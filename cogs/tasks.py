import discord
from discord.ext import commands
from db.tasksdb import TasksDB  # Importa apenas a classe do banco
from db.task_model import Task   # Importa o modelo de forma absoluta

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addtask")
    async def add_task(self, ctx, *, args: str):
        try: 
            title, description = [x.strip() for x in args.split(" | ", 1)]
        except ValueError:
            await ctx.send("⚠️ Formato inválido. Use: `!addtask Título | Descrição`")
            return

        task = Task(user_id=ctx.author.id, title=title, description=description, completed=False)
        await TasksDB.insert_task(task)
        await ctx.send(f"✅ Tarefa adicionada: **{title}**\nDescrição: {description}")

async def setup(bot):
    await bot.add_cog(Tasks(bot))
