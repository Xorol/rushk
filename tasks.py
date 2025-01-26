# Contains the status revolver and word-of-the-day tasks

from extensions.dictionary.dictionary_handler import Dictionary

from interactions import Task, IntervalTrigger, TimeTrigger, Client

from functools import partial
import random


with open("statuses.txt") as status_f:
    STATUSES = status_f.readlines()

TSEVHU_VOCAB_CHANNEL_ID = 742114751064178758


async def status_revolver(client: Client):
    status = random.choice(STATUSES)
    await client.change_presence(activity=status)


async def tsevhu_word_of_the_day(client: Client):
    tsevhu_dictionary = Dictionary("tsevhu")
    word = tsevhu_dictionary.words.choice()

    tsevhu_vocab_channel = await client.fetch_channel(TSEVHU_VOCAB_CHANNEL_ID)
    await word.send(tsevhu_vocab_channel, "", "### Tsevhu word of the day")


async def start_tasks(client: Client):
    status_revolver_task = Task(partial(status_revolver, client), IntervalTrigger(seconds=15))
    tsevhu_word_of_the_day_task = Task(partial(tsevhu_word_of_the_day, client), TimeTrigger(hour=10))

    status_revolver_task.start()
    tsevhu_word_of_the_day_task.start()
