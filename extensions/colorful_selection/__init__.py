import discord
from discord.ext import commands
from extensions.colorful_selection.options_manager import return_response as selection_options


class ColorfulSelection(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Registro de inicialização
    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog colorful_selection está pronta')

    '''
        1. COMANDOS
    '''

    # Ping
    @commands.command()
    async def sel(self, ctx, *, message):
        message = f'$sel {message}'
        response = await selection_options(message, self.client)
        if isinstance(response, tuple):
            if response[1] == True:
                await ctx.channel.purge(limit=1)
                await ctx.channel.send(response[0])
            else:
                await ctx.channel.send(response[0])
                await ctx.channel.send(response[1])
        else:
            await ctx.channel.send(response)


def setup(client):
    client.add_cog(ColorfulSelection(client))
