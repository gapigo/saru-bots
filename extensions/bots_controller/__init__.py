import asyncio

from sqlalchemy.exc import IntegrityError
from discord.ext import commands
from flask_app import db
import random
import json
from bots import running_bots, stopped_bots, get_bots_config, discord_loop, run_bot


class BotsController(commands.Cog):

    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Extension random_messages_tongo was loaded.')


    @commands.command()
    async def stop_bot(self, ctx, *, name=None):
        if not name:
            await ctx.send(f'Informe um nome: .stop_bot [nome]')
            return
        name = name.upper()

        bots_config = get_bots_config()
        if name not in (bot['name'] for bot in bots_config):
            await ctx.send(f'O bot **{name}** não existe no arquivo bot_config.json.')
            return
        task = running_bots.get(name)
        if task and not task.cancelled():
            task.cancel()
            stopped_bots[name] = task
            await ctx.send(f'O bot **{name}** foi parado.')
        await ctx.send(f'O bot **{name}** já estava parado.')

    @commands.command()
    async def start_bot(self, ctx, *, name=None):
        # Check if the user sent a name
        if not name:
            await ctx.send(f'Informe um nome: .start_bot [nome]')
            return

        # Check if the bot is running
        if running_bots.get(name):
            await ctx.send(f'O bot **{name}** já rodando.')
            return

        # Check if the bot exists
        bots_config = get_bots_config()
        bot_config = bots_config.get(name)
        if not bot_config:
            await ctx.send(f'O bot **{name}** não existe no arquivo bot_config.json.')
            return

        run = run_bot(bot_config)
        asyncio.ensure_future(run)
        # asyncio.create_task(run)


def setup(client):
    client.add_cog(BotsController(client))
