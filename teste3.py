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
from async_multitasking import Scheduler
dotenv.load_dotenv()


def run_flask():
    app.run(host="0.0.0.0", port=8080, use_reloader=False)


async def arun_bot(bot_config: dict, loop=None):
    """
    :param bot_config: {
                    "name": "PUDIM",
                    "initial": ["random_messages"]
                }
    """
    print('VEZ')
    token = os.getenv(bot_config['name'] + '_TOKEN')
    bot = lightbulb.BotApp(token=token,
                           prefix='$',
                           banner=None
                           )

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event: hikari.StartedEvent):
        print(f'BOT {str(bot.get_me()):.>20} connected.')

    for extension in bot_config['extensions']:
        # bot.load_extensions_from(f"./extensions/{extension}/main.py")
        bot.load_extensions(f"extensions.{extension}")

    # return bot
    await bot.start()
    print('BULCETA')


def run_bot(bot_config: dict, loop=None):
    """
    :param bot_config: {
                    "name": "PUDIM",
                    "initial": ["random_messages"]
                }
    """
    print('VEZ')
    token = os.getenv(bot_config['name'] + '_TOKEN')
    bot = lightbulb.BotApp(token=token,
                           prefix='$',
                           banner=None
                           )

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event: hikari.StartedEvent):
        print(f'BOT {str(bot.get_me()):.>20} connected.')

    for extension in bot_config['extensions']:
        # bot.load_extensions_from(f"./extensions/{extension}/main.py")
        bot.load_extensions(f"extensions.{extension}")

    # return bot
    # await bot.start()
    # bot.run()
    return bot
    # loop.create_task(await bot.start())
    # return loop


def run_bots():
    sched = Scheduler()
    # run_bots()
    threads = []
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        for bot_config in bots_config:
            print(f'a {bot_config}')
            bot = run_bot(bot_config)
            asyncio.wait(bot.start())
    #         threads.append(Thread(target=bot.run))
    #         # sched.new(run_bot(bot_config))
    #     for thread in threads:
    #         Thread(target=thread.run).start()
    #
    # # sched.mainloop()
    # print(threads)

def run_bots2():
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        # await asyncio.gather(
        #     arun_bot(bots_config[0]),
        #     arun_bot(bots_config[1])
        # )

        start_server = arun_bot(bots_config[0])
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.ensure_future(arun_bot(bots_config[1]))  # before blocking call we schedule our coroutine for sending periodic messages
        asyncio.ensure_future(arun_bot(bots_config[2]))
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    # t1 = Thread(target=run_flask).start()
    if os.name != "nt":
        import uvloop
        uvloop.install()
    # run_bots()
    # asyncio.run(run_bots2())
    run_bots2()

