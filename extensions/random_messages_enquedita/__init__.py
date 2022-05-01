from datetime import datetime
import random
import hikari
import lightbulb
from .models import EnqueditaMessage
from sqlalchemy.exc import IntegrityError
from flask_app import db
from bots import get_general_config

random_messages_enquedita = lightbulb.Plugin("RandomMessagesEnquedita")


def load_messages(type=None):
    messages = []
    if not type:
        for row in EnqueditaMessage.query.all():
            messages.append(row.message)
        return messages


messages = load_messages()
current_hour = datetime.now().hour
MAX = 0.04  # at the peek enquedita will interfere at this percentage (1 = 100%)
last_minute = 0
minutes = [i for i in range(0 + 5, 61, 5)]


def randomize():
    global random_chances, minutes
    random_chances = {}
    max_chance = MAX * random.random()
    min_chance = max_chance / 1000
    len_m = len(minutes)
    chances = []
    i = 0
    increasing_step = (max_chance - min_chance) / len_m
    while i < len_m:
        chances.append(min_chance + increasing_step * i)
        i += 1
    random.shuffle(chances)
    for i, minute in enumerate(minutes):
        random_chances[minute] = chances[i]

randomize()

def set_last_minute(minute):
    global minutes, last_minute
    for min in minutes:
        if minute < min:
            last_minute = min
            break


@random_messages_enquedita.listener(hikari.GuildMessageCreateEvent)
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    global current_hour, random_chances, last_minute, messages
    time = datetime.now()

    if time.hour != current_hour:
        randomize()
    if time.minute > last_minute:
        set_last_minute(time.minute)
    if random.random() < random_chances[last_minute]:
        await event.get_channel().send(random.choice(messages))
        alert_channel = event.get_guild().get_channel(get_general_config().get("alert_channel_id"))
        await alert_channel.send(f'Chance de {random_chances[last_minute]*100}%')
        


@random_messages_enquedita.command
@lightbulb.option(
    "message", "Adiciona a mensagem",
    hikari.Message, required=True
)
@lightbulb.option(
    "type", "Adicione o tom da mensagem.\ntypes: undefined, aggressive, cheerful, funny, sad, nosense, annoying",
    hikari.OptionType, required=False, choices=['undefined', 'aggressive', 'cheerful', 'funny', 'sad', 'nosense',
                                                'annoying']
)
@lightbulb.command(
    "new_enquedita_message", "Adicione uma nova mensagem revolucionária para ajudar a implantação do comunismo."
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def new_enquedita_message(ctx: lightbulb.Context):
    global messages
    type = ctx.options.type if ctx.options.type else 'undefined'
    message = ctx.options.message
    try:
        i = EnqueditaMessage(message, type)
        db.session.add(i)
        db.session.commit()
        messages = load_messages()
        # await ctx.get_channel().send('Nova mensagem revolucionária adicionada. Marx está feliz')
        await ctx.respond('Nova mensagem revolucionária adicionada. Marx está feliz')
    except IntegrityError:
        await ctx.respond("O grande Karl Marx já conhecia essa ai **(๑•́ ₃ •̀๑)**.")


@random_messages_enquedita.command
@lightbulb.command(
    "list_enquedita_messages", "Veja uma densa coletânea dos maiores pensadores desse mundo."
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def list_enquedita_messages(ctx: lightbulb.Context):
    messages_list = ''
    for row in EnqueditaMessage.query.all():
        messages_list += f'{row.id}. {row.message}\n'

    # todo → add a formatted embed paginator
    # current showing the last 2 thousand characters only
    await ctx.respond(messages_list[-2000:])
#
@random_messages_enquedita.command
@lightbulb.option(
    "index", "Mostre pro enquedita o index que você quer deletar (veja mais com .list_enquedita_messages)",
    hikari.Message, required=True
)
@lightbulb.command(
    "delete_enquedita_message", "Deconstrua o pensamento, apagando mensagens patriarcais obsoletas."
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def delete_enquedita_message(ctx: lightbulb.Context):
    index = ctx.options.index if ctx.options.index else None
    if index is None:
        await ctx.respond('Fale para mim qual mensagem você quer deletar, precisamos de números para impor a revolução!\n\n'
                       '-> delete_enquedita_message [index]')
    try:
        tongo_message = EnqueditaMessage.query.filter_by(id=index).first()
        db.session.delete(tongo_message)
        db.session.commit()
        await ctx.respond('Mensagem patriarcar apagada!')
    except:
        await ctx.respond('Não consegui entender, por favor informe o número para apagarmos o machismo')


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(random_messages_enquedita)
