###########
#LIBRARIES#
###########

import interactions  # discord api wrapper
import os  # You know what this is
import asyncio
import utils  # custom module, in folder named utils
import random  # You also know what this is
import logging  # Helps with debugging
from interactions.ext.tasks import IntervalTrigger, create_task  # Task extension
from interactions.ext.wait_for import setup
from loguru import logger
from interactions.api.http.route import Route

#######
#DEBUG#
#######

logging.basicConfig(level=logging.DEBUG)

#####
#BOT#
#####

bot: interactions.Client = interactions.Client(
    token=os.environ["token"],  # Token secret
    #disable_sync = True
)

# Comes from the wait_for extension,
# Applies hooks to the class
setup(bot)

send_start_up_msg = False
on_start_msg = "Added some more statuses (statii?)"
start_msg_channel_name = "bot"

bot_name = "Rushk but hip"

##################
#REVOLVING STATUS#
##################

# List of available statuses (statii?) to rotate through
with open("statuses.txt", "r") as f:
  status_wheel = f.readlines()


# Makes it switch every 15 seconds
@create_task(IntervalTrigger(15))
async def switch_statuses():
    status = random.choice(status_wheel)
    await utils.bot.set_game(status, bot)


##########
#ON READY#
##########


@bot.event()
async def on_ready():

    # Get all guilds the bot is in
    guilds = bot.guilds

    # Print thing
    print(
        f"[{utils.time.get_formatted_time()}] Joining {guilds[0]} as {bot_name}!"
    )

    # Send a start-up message
    if send_start_up_msg:
        start_msg_channel = await utils.bot.get_channel(
            bot, start_msg_channel_name)
        await start_msg_channel.send(on_start_msg)
        print(
            f"[{utils.time.get_formatted_time()}] Start-up message sent successfully to #{start_msg_channel_name}!\n{on_start_msg}"
        )
    else:
        print(
            f"[{utils.time.get_formatted_time()}] A start-up message was not sent successfully!"
        )

    # Set an initial status
    await utils.bot.set_game(
        "You've seen me within 15 seconds of me starting up! You must be a true fan!",
        bot)

    # Begin the status revolver
    switch_statuses.start()
    print(f"[{utils.time.get_formatted_time()}] Status revolver started!")


##############################
#COMMAND & BOT INITIALIZATION#
##############################

#Command Module initialization
bot.load("commands.dictionary")
print(f"[{utils.time.get_formatted_time()}] Dictionary commands loaded!")
bot.load("commands.fun")
print(f"[{utils.time.get_formatted_time()}] Fun commands loaded!")
bot.load("commands.wikipedia")
print(f"[{utils.time.get_formatted_time()}] Wikipedia commands loaded!")
bot.load("commands.suggestions")
print(f"[{utils.time.get_formatted_time()}] Suggestion commands loaded!")
bot.load("commands.language")
print(f"[{utils.time.get_formatted_time()}] Language commands loaded!")
bot.load("commands.tsevhu")
print(f"[{utils.time.get_formatted_time()}] Tsevhu commands loaded!")

#more debugging
#async def get_self_guilds():
#    request = await bot._http._req.request(Route("GET", "/users/@me/guilds"))
#    print("==> REQUEST:", request)
#asyncio.run(get_self_guilds())

# Initialize the bot
#with logger.catch():
#   bot.start()

bot.start()
