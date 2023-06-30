import interactions
from os import environ
import utils
import random
import asyncio

bot = interactions.Client(delete_unused_application_cmds=True)

dicts = utils.load_dictionaries()
word_amt = 0
for dict in dicts:
  word_amt += utils.Dictionary(dict, dicts).length
dict_amt = str(len(dicts))
word_amt = str(word_amt)
del dicts


with open("extensions.txt", "r") as extf:
      EXTENSIONS = extf.read().splitlines(False)

with open("statuses.txt", "r") as statuses_file:
  statuses = statuses_file.readlines()

@interactions.Task.create(interactions.IntervalTrigger(seconds=15)) 
async def set_status():
    new_status = random.choice(statuses).replace("{words}", word_amt).replace("{dictamt}", dict_amt)
    await utils.set_game(new_status, bot)

@interactions.listen()
async def on_startup():
    print("Bot is ready!")
    set_status.start()

for i in EXTENSIONS:
  bot.load_extension(i)


bot.start(environ["TOKEN"])
