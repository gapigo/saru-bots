import asyncio
import os
from pathlib import Path
from sqlalchemy.exc import IntegrityError
from discord.ext import commands
from flask_app import db
import random
import json
from bots import running_bots, get_bots_config, run_bot

extension_name = os.path.basename(Path(__file__).parent.absolute())
# Define who is the bot who runs this extension
def get_extension_owner():
    bots_config = get_bots_config(lower=True)
    for bot_name, bot_config in bots_config.items():
        if extension_name in bot_config.get('extensions'):
            return bot_name


class BotsController(commands.Cog):

    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Extension random_messages_tongo was loaded.')


    @commands.command()
    async def stop_bot(self, ctx, *, name: str = None):
        # Check if the user sent a name
        if not name:
            print(running_bots)
            # print(running_bots['anano_moura'].__dir__())
            # print(await running_bots.get('anano_moura').close())
            await ctx.send(f'Informe um nome: .stop_bot [nome]')
            return

        name = name.lower()
        # Check if the bot exists
        bots_config = get_bots_config(lower=True)
        bot_config = bots_config.get(name)
        if not bot_config:
            await ctx.send(f'O bot **{name}** não existe no arquivo bot_config.json.')
            return

        # task = running_bots.get(name)
        # if task and not task.cancelled():
        #     task.cancel()
        #     stopped_bots[name] = task
        #     await ctx.send(f'O bot **{name}** foi parado.')

        # Check if the bot is the owner of this extension
        if get_extension_owner() == name:
            await ctx.send(f'O bot **{name}** é dono da extensão {extension_name}, não é possível pará-lo pois ele '
                           f'assumiu o papel de "administrador".')
            return

        # Check if the bot is not running
        if not running_bots.get(name):
            await ctx.send(f'O bot **{name}** já está parado.')
            return

        # print(ctx.command.__dir__())
        # bot_id = get_bot_id(name)
        await running_bots.get(name).close()
        await ctx.send(f'O bot **{name}** foi parado.')
        running_bots.pop(name)

    @commands.command()
    async def start_bot(self, ctx, *, name: str = None):
        # Check if the user sent a name
        if not name:
            await ctx.send(f'Informe um nome: .start_bot [nome]')
            return

        name = name.lower()

        # Check if the bot is running
        if running_bots.get(name):
            await ctx.send(f'O bot **{name}** já rodando.')
            return

        # Check if the bot exists
        bots_config = get_bots_config(lower=True)
        bot_config = bots_config.get(name)
        if not bot_config:
            await ctx.send(f'O bot **{name}** não existe no arquivo bot_config.json.')
            return

        # Check if bot is disabled
        if bot_config.get("disabled"):
            await ctx.send(f'O bot **{name}** não pode ser iniciado pois está desativado dentro de bot_config.json')

        run = run_bot(name, bot_config)
        asyncio.ensure_future(run)  # the bot is appended in running_bots inside this function
        # asyncio.create_task(run)


def setup(client):
    client.add_cog(BotsController(client))
