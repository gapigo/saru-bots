import sqlite3
import discord
import json
from sqlalchemy.exc import IntegrityError
from discord.ext import commands
from .models import TongoMessage
from flask_app import db
import random


class RandomMessagesTongo(commands.Cog):

    def __init__(self, client):
        self.bot = client
        self.messages = self.load_messages()
        self.trigger_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

    @commands.Cog.listener()
    async def on_ready(self):
        print('Extension random_messages_tongo was loaded.')

    @staticmethod
    def load_messages(type=None):
        messages = []
        if not type:
            for row in TongoMessage.query.all():
                messages.append(row.message)
            return messages

    # if msg.startswith("$new"):
    #     encouraging_message = msg.split("$new ", 1)[1]
    #     update_enrouragements(encouraging_message)
    #     await message.channel.send("New encouraging message added.")

    @commands.command()
    async def new_tongal_message(self, ctx, *, params):
        type = 'undefined'
        if '--type' in params:
            content = params.split('--type')[1].strip()
            words: list = content.split(' ')
            type = words.pop(0)
            message = ' '.join(words)
        else:
            message = params.strip()
        try:
            i = TongoMessage(message, type)
            db.session.add(i)
            db.session.commit()
            self.messages = self.load_messages()
            await ctx.send("Nova zueirinha tongalesca aprendida.")
        except IntegrityError:
            await ctx.send("Tongo já conhece essa zuerinha, nom fo adiciona 	**(*￣▽￣)b**.")

    @commands.command()
    async def list_tongal_messages(self, ctx, *, params=None):
        messages_list = ''
        for row in TongoMessage.query.all():
            messages_list += f'{row.id}. {row.message}\n'

        # todo → add a formatted embed paginator
        # current showing the last 2 thousand characters only
        await ctx.send(messages_list[-2000:])

    @commands.command()
    async def delete_tongal_message(self, ctx, index=None):
        if index is None:
            await ctx.send('Fala po tongo cual mensage vc quer deletar animal\n\n'
                           '-> delete_tongal_message [index]')
        try:
            tongo_message = TongoMessage.query.filter_by(id=index).first()
            db.session.delete(tongo_message)
            db.session.commit()
            await ctx.send('Tongo deleto mesagezita :)))))))))')
        except:
            await ctx.send('Tongo nom deletar nata poke tongo nom entender')

    @commands.Cog.listener("on_message")
    async def send_tongal(self, message):
        msg = message.content
        if any(word in msg for word in self.trigger_words):
            await message.channel.send(random.choice(self.messages))

    # async def on_message(self, message):
    #     print(message.content)






def setup(client):
    client.add_cog(RandomMessagesTongo(client))
