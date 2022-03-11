import asyncio
import dotenv
import hikari
import json
import lightbulb
import os
from discord.ext import commands

dotenv.load_dotenv()
DEFAULT_PREFIX = '$'


def print_console_on_online(bot_name):
    print(f'BOT {str(bot_name):.>20} connected.')


def get_prefix(bot_config: dict) -> str:
    if (prefix := bot_config.get('prefix')) is None:
        return DEFAULT_PREFIX
    return prefix


def get_token(bot_config: dict) -> str:
    return os.getenv(bot_config['name'] + '_TOKEN')


async def run_hikari(bot_config: dict) -> None:
    # token = os.getenv(bot_config['name'] + '_TOKEN')
    token = get_token(bot_config)
    bot = lightbulb.BotApp(token=token,
                           prefix=get_prefix(bot_config),
                           banner=None,
                           # default_enabled_guilds=os.getenv('GUILD_ID')
                           )

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event: hikari.StartedEvent):
        # print(f'BOT {str(bot.get_me()):.>20} connected.')
        bot_name = str(bot.get_me()).split('#')[0]
        print_console_on_online(bot_name)
        if bot_config.get('notify_if_online'):
            channel = await bot.rest.fetch_channel('425222899104874507')
            await channel.send('O símbolo paterno está online.')

        for extension in bot_config['extensions']:
            try:
                bot.load_extensions(f"extensions.{extension}")
            except lightbulb.errors.ExtensionMissingLoad:
                print(f"BOT {bot_name}: The extension '{extension}' is not a valid 'hikari.py' extension.")
            except lightbulb.errors.CommandAlreadyExists:
                print(f"BOT {bot_name}: The extension 'hikari.py' '{extension}' has commands that are already taken.")

    await bot.start()


async def run_dpy(bot_config: dict):
    bot = commands.Bot(command_prefix=get_prefix(bot_config))

    @bot.event  # Evento de inicialização
    async def on_ready():  # Emite um registro no console se o bot está
        # print(f'{client.user.name} está pronto.')  # Rodando ou não
        bot_name = bot.user.name
        print_console_on_online(bot_name)

        if bot_config.get('notify_if_online'):
            # channel = await bot.rest.fetch_channel('425222899104874507')
            # await channel.send('O símbolo paterno está online.')
            ...

        for extension in bot_config['extensions']:
            try:
                bot.load_extension(f"extensions.{extension}")
            except commands.errors.NoEntryPointError:
                print(f"BOT {bot_name}: The extension '{extension}' is not a valid 'discord.py' extension.")
            except commands.errors.CommandRegistrationError:
                print(f"BOT {bot_name}: The extension 'discord.py' '{extension}' has commands that are already taken.")

    token = get_token(bot_config)
    await bot.start(token)


async def run_bot(bot_config: dict):
    """
    :param bot_config: {
                    "name": "PUDIM",
                    "initial": ["random_messages"]
                }
    """
    if bot_config.get('library') == 'discord.py':
        await run_dpy(bot_config)
    else:
        await run_hikari(bot_config)


def run_bots():
    with open('bot_config.json') as f:
        bots_config = json.load(f)
        # for num, bot_config in enumerate(bots_config):
        #     run = run_bot(bot_config)
        #     if num == 0:
        #         asyncio.get_event_loop().run_until_complete(run)
        #     else:
        #         asyncio.ensure_future(run)
        asyncio.get_event_loop()
        for bot_config in bots_config:
            run = run_bot(bot_config)
            asyncio.ensure_future(run)
    asyncio.get_event_loop().run_forever()


"""
https://stackoverflow.com/questions/32054066/
python-how-to-run-multiple-coroutines-concurrently-using-asyncio#
:~:text=You%20can%20use%20asyncio.,call%20for%20starting%20event%20loop.
"""
