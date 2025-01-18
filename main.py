import dotenv

from interactions import Client, Intents, listen

from tasks import start_tasks

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    await start_tasks(bot)
    print("Ready")
    print(f"This bot is owned by {bot.owner}")
    print(bot.application_commands)


bot.load_extension("extensions.dictionary.dictionary_ext")
bot.load_extension("extensions.tsevhu.tsevhu_ext")
bot.load_extension("extensions.fun_ext")

# Get the token and start the bot
TOKEN = dotenv.dotenv_values(".env")["TOKEN"]

bot.start(TOKEN)