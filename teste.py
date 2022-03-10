import os
# import extensions.info

import dotenv
import hikari
import lightbulb

dotenv.load_dotenv()

bot = lightbulb.BotApp(
    os.environ["PUDIM_TOKEN"],
    prefix="+",
    banner=None,
    default_enabled_guilds=(338045183558156289,)
    # intents=hikari.Intents.ALL,
)


@bot.command
@lightbulb.command("ping", description="The bot's ping")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")



if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()
    available_extensions: list = next(os.walk('./extensions'))[1]
    available_extensions.remove('__pycache__')
    print(available_extensions)
    for extension in available_extensions:
        # bot.load_extensions_from(f"./extensions/{extension}/main.py")
        bot.load_extensions(f"extensions.{extension}")
    # bot.load_extensions_from(f"./extensions/")
    bot.run()
