import asyncio
import dotenv
import hikari
import json
import lightbulb
import os

dotenv.load_dotenv()


async def run_bot(bot_config: dict):
    """
    :param bot_config: {
                    "name": "PUDIM",
                    "initial": ["random_messages"]
                }
    """
    token = os.getenv(bot_config['name'] + '_TOKEN')
    bot = lightbulb.BotApp(token=token,
                           prefix='$',
                           banner=None,
                           # default_enabled_guilds=os.getenv('GUILD_ID')
                           )

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event: hikari.StartedEvent):
        print(f'BOT {str(bot.get_me()):.>20} connected.')
        if bot_config.get('notify_if_online'):
            channel = await bot.rest.fetch_channel('425222899104874507')
            await channel.send('O símbolo paterno está online.')

    for extension in bot_config['extensions']:
        bot.load_extensions(f"extensions.{extension}")

    await bot.start()


def run_bots():
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        for num, bot_config in enumerate(bots_config):
            run = run_bot(bot_config)
            if num == 0:
                asyncio.get_event_loop().run_until_complete(run)
            else:
                asyncio.ensure_future(run)
    asyncio.get_event_loop().run_forever()


"""
https://stackoverflow.com/questions/32054066/
python-how-to-run-multiple-coroutines-concurrently-using-asyncio#
:~:text=You%20can%20use%20asyncio.,call%20for%20starting%20event%20loop.
"""
