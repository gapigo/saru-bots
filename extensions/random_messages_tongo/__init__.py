import discord
from discord.ext import commands


class RandomMessagesTongo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Extension random_messages_tongo was loaded.')


def setup(client):
    client.add_cog(RandomMessagesTongo(client))
