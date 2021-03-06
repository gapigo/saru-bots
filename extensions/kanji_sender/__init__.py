import datetime
from .kanji_web_scrapping import search_kanji
from .is_cjk import is_kanji
from discord.ext import commands
import os
from pathlib import Path
from bots import get_general_config
import discord

KANJI_CHANNEL_ID = '839084585760587797'

class ComandosSimples(commands.Cog):

    def __init__(self, client):
        self.bot = client
    
    def get_channel(self, ctx):
        # if kanji_channel := os.getenv('kanji_channel'):
        if os.environ.get('DEBUG'):
            selected_channel = get_general_config().get('test_channel')
        else:
            selected_channel = get_general_config().get('kanji_channel')
        if kanji_channel := selected_channel:
            if kanji_channel.isnumeric() and len(kanji_channel) == 18:
                c_channel = discord.utils.get(ctx.guild.text_channels, id=kanji_channel)
            else:
                c_channel = discord.utils.get(ctx.guild.text_channels, name=kanji_channel)
            return c_channel
        else:
            raise ValueError('kanji_channel not found in general_config.json, inform the id or the name of a real channel of your server')

    async def print_date(self, ctx):
        # c_channel = discord.utils.get(ctx.guild.text_channels, name='🎌│kanji_diário-毎日の漢字')
        c_channel = self.get_channel(ctx)
        messages = await c_channel.history(limit=10).flatten()
        count = 0
        current_date: datetime
        for message in messages:
            msg: str = message.content
            if msg.startswith('**') and is_kanji(msg[2]):
                count += 1
            elif msg.startswith('```fix'):
                current_date_str = msg.split('\n')[2]
                current_date = datetime.datetime.strptime(current_date_str, '%d/%m/%Y')
                break
        send_new_date = ''
        if count >= 5:
            current_date = current_date + datetime.timedelta(days=1)
            send_new_date += '```fix\n' \
                             'KANJIS DO DIA\n' \
                             f'{current_date.strftime("%d/%m/%Y")}\n' \
                             '```'
        if send_new_date:
            await ctx.channel.send(send_new_date)

    # @commands.command()
    # async def teste(self, ctx):
    #     await self.print_date(ctx)

    @commands.Cog.listener("on_message")
    async def send_kanji(self, ctx):
        fetched_channel = self.get_channel(ctx)
        if str(ctx.channel.id) == str(fetched_channel.id):
            msg = ctx.content
            if len(msg) == 1 and is_kanji(msg):
                await ctx.channel.purge(limit=1)
                await self.print_date(ctx)
                message = await ctx.channel.send(f'Pesquisando **{msg}**...')
                generator = search_kanji(ctx.content)
                for res in generator:
                    if type(res) == str:
                        await message.edit(content=res)
                    else:
                        await message.edit(content="Loading...")
                        # res
                        # {'kanji': '歳',
                        # 'plataform': 'romajidesu',
                        # 'onyomi': 'サイ、セイ',
                        # 'kunyomi': 'とし、とせ、よわい',
                        # 'meaning': 'year-end, age, occasion, opportunity',
                        # 'link': 'http://www.romajidesu.com/kanji/%E6%AD%B3'}
                        if res.get('plataform') == 'nihongoichiban':
                            img = 'nihongoichiban.gif'
                        elif res.get('plataform') == 'romajidesu':
                            img = 'romajidesu.png'
                        # elif res.get('plataform') == 'romanjitanoshii':
                        else:
                            img = 'tanoshiijapanese.png'  
                        # img = 'nihongoichiban.gif' if res.get('plataform') == 'nihongoichiban' else 'romajidesu.png'
                        fmsg = f'''**{res.get('kanji')}**\n        
音読み
{res.get('onyomi') if res.get('onyomi') else '-'}

訓読み
{res.get('kunyomi') if res.get('kunyomi') else '-'}

Meaning: {res.get('meaning')}
{res.get('link')}'''
                        await ctx.channel.purge(limit=1)
                        await ctx.channel.send(content=fmsg,
                                               file=discord.File(os.path.join(Path(__file__).parent.absolute(), f'images/{img}')))

def setup(client):
    client.add_cog(ComandosSimples(client))
