import asyncio
import pprint
import os
import json
import hikari
from flask_app import app
from threading import Thread
import dotenv
import lightbulb
dotenv.load_dotenv()

def run_flask():
    app.run(host="0.0.0.0", port=8080, use_reloader=False)

async def run_client(bot_name):
    token = os.getenv(bot_name + '_TOKEN')
    # bot = lightbulb.BotApp(token, intents=hikari.Intents.ALL)
    bot = lightbulb.BotApp(token=token,
                           prefix='$',
                           banner=None
                           # intents=hikari.Intents.ALL,
                           # default_enabled_guilds=os.getenv('GUILD_ID')
                           )
    # bot = hikari.GatewayBot(token)

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event):
        print(f'BOT {str(bot.get_me()):.>20} connected.')
        channel = await bot.rest.fetch_channel('425222899104874507')
        await channel.send('O símbolo paterno está online.')

    # @bot.command
    # @lightbulb.command("ping", description="The bot's ping")
    # @lightbulb.implements(lightbulb.PrefixCommand)
    # async def ping(ctx) -> None:
    #     await ctx.respond(f"Pong! Latency: ms")

    @bot.listen(hikari.GuildMessageCreateEvent)
    async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
        # if event.is_bot or not event.content:
        #     return

        # if event.content.strip() == "+ping":
        #     await event.message.respond(
        #         f"Pong! Latency: {bot.heartbeat_latency * 1000:.2f}ms"
        #     )
        # channel = await bot.rest.fetch_channel('425222899104874507')
        # await channel.send(event)
        # await channel.send(event.content)
        # await channel.send(event.content.strip())
        print(event)

    # bot.load_extensions_from("./extensions")

    await bot.start()

async def run_discord():
    bots = []
    with open('bot_config.json') as f:
        bot_config = json.load(f)
        for bot in bot_config:
            bots.append(run_client(bot['name']))
    await asyncio.gather(*bots)

t1 = Thread(target=run_flask).start()

if os.name != "nt":
    import uvloop
    uvloop.install()

asyncio.run(run_discord())

'''
Discord running multiple bots:
https://stackoverflow.com/questions/64733654/runtimeerror-when-multithreading-python-runtimeerror-there-is-no-current-event
'''
