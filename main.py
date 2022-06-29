###########
#LIBRARIES#
###########

import interactions  # discord api wrapper
import os  # You know what this is
import utils  # custom module, in folder named utils
import random  # You also know what this is
import logging  # Helps with debugging
from interactions.ext.tasks import IntervalTrigger, create_task  # Task extension
from interactions.ext.wait_for import setup # Wait-for extension

#######
#DEBUG#
#######

logging.basicConfig(level=logging.WARNING)

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

bot_name = "Rushk but hip"

##################
#REVOLVING STATUS#
##################

# List of available statuses (statii?) to rotate through
with open("statuses.txt", "r") as f:
  status_wheel = f.readlines()


# Makes it switch statuses every 15 seconds
@create_task(IntervalTrigger(15))
async def switch_statuses():
    status = random.choice(status_wheel)
    await utils.utils.set_game(status, bot)


##########
#ON READY#
##########


@bot.event()
async def on_ready():

    # Get all guilds the bot is in
    guilds = bot.guilds

    # Print join message
    utils.ts_print(
        f"[%s] Joining {guilds[0]} as {bot_name}!"
    )

    # Set an initial status
    await utils.utils.set_game(
        "You've seen me within 15 seconds of me starting up! You must be a true fan!",
        bot
        )

    # Begin the status revolver
    switch_statuses.start()
    utils.ts_print("[%s] Status revolver started!")


##############################
#COMMAND & BOT INITIALIZATION#
##############################

# Open extensions file
with open("extensions.txt", "r") as fexts:
    exts: list[str] = fexts.read().split("\n")

for i in exts:
    bot.load(f"commands.{i}")
    utils.time.ts_print(f"[%s] Loaded extension '{i}'")

# Start the bot
bot.start()
