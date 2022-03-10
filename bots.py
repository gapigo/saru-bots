import asyncio
import dotenv
import hikari
import json
import lightbulb
import os

dotenv.load_dotenv()


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
