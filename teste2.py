import os
# import extensions.info
import dotenv
import hikari
import lightbulb
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


async def run_bot(bot_config: dict, loop=None):
    """
    :param bot_config: {
                    "name": "PUDIM",
                    "initial": ["random_messages"]
                }
    """

    token = os.getenv(bot_config['name'] + '_TOKEN')
    bot = lightbulb.BotApp(token=token,
                           prefix='$',
                           banner=None
                           )

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event: hikari.StartedEvent):
        print(f'BOT {str(bot.get_me()):.>20} connected.')
        # channel = await bot.rest.fetch_channel('425222899104874507')
        # await channel.send('O símbolo paterno está online.')


    # @bot.listen(hikari.GuildMessageCreateEvent)
    # async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    #     print(event)
    # available_extensions: list = next(os.walk('./extensions'))[1]
    # available_extensions.remove('__pycache__')
    # for extension in available_extensions:
    for extension in bot_config['extensions']:
        # bot.load_extensions_from(f"./extensions/{extension}/main.py")
        bot.load_extensions(f"extensions.{extension}")

    # await bot.start()
    return bot
    # loop.create_task(await bot.start())
    # return loop


async def run_bots():
    bots = []
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        for bot_conf in bots_config:
            print('A' + bot_conf['name'])
            bots.append(run_bot(bot_conf))
            # bot = await run_bot(bot_conf)
            # await bot.start()
            # # print(bot.__dir__())
    # print(bots)
    await asyncio.gather(*bots)


async def run_bots2():
    bots = []
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        # for bot_conf in bots_config:
        #     print('A' + bot_conf['name'])
        #     bots.append(run_bot(bot_conf))
        print('Rodando o primeiro bot...')
        await run_bot(bots_config[0])
        print('Rodando o segundo bot...')
        await run_bot(bots_config[1])

    # await asyncio.gather(*bots)


async def run_bots3():
    # bots = []
    loop = asyncio.get_event_loop()
    # loop.create_task(client1.start('TOKEN1'))
    # loop.create_task(client2.start('TOKEN2'))
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        for bot_conf in bots_config:
            print('A' + bot_conf['name'])
            # bots.append(run_bot(bot_conf))
            loop = await run_bot(bot_conf, loop)
    # print(f'ASPODKASPDOK {loop.}')
    loop.run_forever()
    # print(bots)
    # await asyncio.gather(*bots)


async def run_bots4():
    bots = []
    loop = asyncio.get_event_loop()
    # loop.create_task(client1.start('TOKEN1'))
    # loop.create_task(client2.start('TOKEN2'))
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        for bot_conf in bots_config:
            print('A' + bot_conf['name'])
            # bots.append(run_bot(bot_conf))
            bots.append(run_bot(bot_conf))
    # print(f'ASPODKASPDOK {loop.}')
    # loop.run_forever()
    # print(bots)
    # await asyncio.gather(*bots)
    # for bot in bots:
    #     loop.create_task(bot.)


'''
Discord running multiple bots:
https://stackoverflow.com/questions/64733654/runtimeerror-when-multithreading-python-runtimeerror-there-is-no-current-event
'''

if __name__ == "__main__":
    # t1 = Thread(target=run_flask).start()
    if os.name != "nt":
        import uvloop
        uvloop.install()

    # asyncio.run(run_bots())
    # asyncio.run(run_bots2())
    # asyncio.run(run_bots3())
    # run_bots3()
    # loop = asyncio.get_event_loop()
    # asyncio.wait(await run_bots2())