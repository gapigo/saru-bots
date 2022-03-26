import asyncio
import dotenv
import hikari
import json
import lightbulb
import os
from discord.ext import commands

dotenv.load_dotenv()
DEFAULT_PREFIX = '$'
running_bots = {
    # 'BOT_NAME': task_object
}
discord_loop = None


def add_bot_to_running_bots(bot_name: str, bot):
    running_bots[bot_name.lower()] = bot


def get_bots_config(lower: bool = False) -> dict:
    with open('bot_config.json', encoding='utf-8') as j:
        available_bots = {}
        bots_config: dict = json.load(j)
        for bot_name, bot_config in bots_config.items():
            if os.getenv('DEBUG'):
                if bot_config.get('debug'):
                    available_bots[bot_name.lower() if lower else bot_name] = bot_config
            else:
                if not bot_config.get('disabled'):
                    available_bots[bot_name.lower() if lower else bot_name] = bot_config
        return available_bots


def get_general_config() -> dict:
    with open('general_config.json', encoding='utf-8') as j:
        general_config = json.load(j)
        return general_config


def print_console_on_online(bot_name):
    print(f'BOT {str(bot_name):.>20} connected.')


def get_prefix(bot_config: dict) -> str:
    if (prefix := bot_config.get('prefix')) is None:
        return DEFAULT_PREFIX
    return prefix


def get_token(bot_name: str) -> str:
    key: str = bot_name + '_TOKEN'
    key = key.upper()
    token = os.getenv(key)
    if not token:
        raise NameError(key + '_TOKEN not found in the environment.')
    return token


def get_bot_id(bot_name: str) -> str:
    key: str = bot_name + '_ID'
    key = key.upper()
    bot_id = os.getenv(key)
    if not bot_id:
        raise NameError(f'{bot_name}_ID not found in the environment.')
    return bot_id


def get_all_extensions() -> list:
    rootdir = os.path.dirname(__file__)
    extensions = os.path.join(rootdir, 'extensions')
    all_extensions = []
    for file in os.listdir(extensions):
        if str(file).endswith('.py'):
            file = file[:-2]
        all_extensions.append(file)
    return all_extensions


async def run_hikari(bot_name: str, bot_config: dict) -> None:
    token = get_token(bot_name)
    bot = lightbulb.BotApp(token=token,
                           prefix=get_prefix(bot_config),
                           banner=None,
                           # default_enabled_guilds=os.getenv('GUILD_ID')
                           )

    @bot.listen(hikari.StartedEvent)
    async def bot_started(event: hikari.StartedEvent):
        print_console_on_online(bot_name)
        if bot_config.get('notify_if_online'):
            channel = await bot.rest.fetch_channel(get_general_config().get("alert_channel_id"))
            hi_msg = bot_config.get('connect_msg')
            await channel.send(hi_msg if hi_msg else get_general_config().get("connect_default_message"))

        all = False
        if bot_config['extensions'] == ['all']:
            bot_config['extensions'] = get_all_extensions()
            all = True
            print('Hikari.py - Extensions loaded: ', end='')

        for extension in bot_config['extensions']:
            try:
                bot.load_extensions(f"extensions.{extension}")
                if all:
                    print(extension, end=", ")
            except lightbulb.errors.ExtensionMissingLoad:
                if not all:
                    print(f"BOT {bot_name}: The extension '{extension}' is not a valid 'hikari.py' extension.")
            except lightbulb.errors.CommandAlreadyExists:
                if not all:
                    print(f"BOT {bot_name}: The extension 'hikari.py' '{extension}' has commands that are already taken.")
        add_bot_to_running_bots(bot_name, bot)

    @bot.listen(hikari.StoppingEvent)
    async def on_stopping(event: hikari.StoppingEvent):
        channel = await bot.rest.fetch_channel(get_general_config().get("alert_channel_id"))
        bye_msg = bot_config.get('shutdown_msg')
        await channel.send(bye_msg if bye_msg else get_general_config().get("shutdown_default_message"))

    await bot.start()


async def run_dpy(bot_name: str, bot_config: dict):
    bot = commands.Bot(command_prefix=get_prefix(bot_config))

    @bot.event  # Evento de inicialização
    async def on_ready():  # Emite um registro no console se o bot está
        print_console_on_online(bot_name)

        if bot_config.get('notify_if_online'):
            channel = await bot.fetch_channel(get_general_config().get("alert_channel_id"))
            hi_msg = bot_config.get('connect_msg')
            await channel.send(hi_msg if hi_msg else get_general_config().get("connect_default_message"))

        all = False
        if bot_config['extensions'] == ['all']:
            bot_config['extensions'] = get_all_extensions()
            all = True
            print('Discord.py - Extensions loaded: ', end='')

        for extension in bot_config['extensions']:
            try:
                bot.load_extension(f"extensions.{extension}")
                if all:
                    print(extension, end=", ")

            except commands.errors.NoEntryPointError:
                if not all:
                    print(f"BOT {bot_name}: The extension '{extension}' is not a valid 'discord.py' extension.")
            except commands.errors.CommandRegistrationError:
                if not all:
                    print(f"BOT {bot_name}: The extension 'discord.py' '{extension}' has commands that are already taken.")

        add_bot_to_running_bots(bot_name, bot)

    @bot.event  # Evento de desligamento
    async def on_disconnect():
        channel = await bot.fetch_channel(get_general_config().get("alert_channel_id"))
        bye_msg = bot_config.get('shutdown_msg')
        await channel.send(bye_msg if bye_msg else get_general_config().get("shutdown_default_message"))

    token = get_token(bot_name)
    await bot.start(token)


async def run_bot(bot_name: str, bot_config: dict):
    """
    :param bot_config: {
                    "name": "PUDIM",
                    "initial": ["random_messages"]
                }
    """
    if bot_config.get('library') == 'discord.py':
        await run_dpy(bot_name, bot_config)
    else:
        await run_hikari(bot_name, bot_config)


def run_bots():
    global discord_loop, running_bots
    bots_config: dict = get_bots_config()
    discord_loop = asyncio.get_event_loop()  # initializing the async loop
    for bot_name, bot_config in bots_config.items():
        run = run_bot(bot_name, bot_config)
        asyncio.ensure_future(run)
    discord_loop.run_forever()


"""
https://stackoverflow.com/questions/32054066/
python-how-to-run-multiple-coroutines-concurrently-using-asyncio#
:~:text=You%20can%20use%20asyncio.,call%20for%20starting%20event%20loop.
"""
