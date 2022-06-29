import interactions
import datetime as dt
import json
import random

TIMESTAMP_FORMAT = "%H:%M:%S"

PUNCTUATION = [
  ".",
  ",",
  ";",
  "!",
  ":",
  "?",
  "(",
  ")",
  "&",
  "/"
]

KOILANG_CHANNEL_IDS = {
  "bot": 773676901146296320
}

KOILANG = 719617569908064348
XOROL = 938379645919834143

class Dictionary:
  def __init__(self, name : str, dictionaries : dict):
    self.file = dictionaries[name]["file"]
    
    with open(self.file) as f:
      self.raw = f.read()

    dictionary = dictionaries[name]
    self.owner = dictionary['owner']
    self.description = dictionary['description']
    self.name = dictionary['name']
    self.display_name = dictionary['display']
    self.link = dictionary['dictionary']
    self.image = dictionary['image']

    self.words = [i.split(',')[:4] for i in self.raw.split("\n")]

  def search (self, item : str, specificity : str = "broad"):
    out = []
    if specificity == "broad":
      for i in self.words:
        for j in i:
          if item in j: 
            out.append(i)
    elif specificity == "narrow":
      for i in self.words:
        for j in i:
          if item == j: 
            out.append(i)

    if len(out) == 0:
      return "No results"

    act_out = f"Result{'s' if len(out) > 1 else ''} for {item} in {self.display_name}:"
    
    for i in out:
      act_out += "\n" + self.format_word(i)

    return act_out

  def format_word(self, word, oneline : bool = False):
    return f"**{word[0]}** {'/' if word[1] else ''}{word[1]}{'/' if word[1] else ''} - {word[2]}. {word[3]}" if oneline else f"**{word[0]}** {'/' if word[1] else ''}{word[1]}{'/' if word[1] else ''}\n*{word[2]}*. {word[3]}"

  def random_word(self, oneline : bool = False):
    return self.format_word(random.choice(self.words), oneline)

def load_dictionaries():
  with open('dictionaries/dictionaries.json') as f:
    return json.load(f)

def generate_dictionary_choices():
  dicts = load_dictionaries()
  out = []
  for i in dicts.keys():
    out.append(interactions.Choice(name = dicts[i]['display'], value = dicts[i]['name']))
  return out

async def set_game(game : str, client : interactions.Client):
  await client.change_presence(interactions.ClientPresence(activities=[interactions.PresenceActivity(name=game, type=interactions.PresenceActivityType.GAME)]))

async def get_user (id : int, client : interactions.Client):
  return interactions.User(**await client._http.get_user(id), _client=client._http)

async def get_channel(client : interactions.Client, channel_name : str):
  """
  Creates a channel object correspoding to `channel_name`, to which messages can be sent and stuff
  """
  
  return interactions.Channel( # turns it into a channel object
    ** await client._http.get_channel(KOILANG_CHANNEL_IDS[channel_name]), # Gets the channel
    _client = client._http
  )

def get_formatted_time():
  """
  Returns the currrent UTC hour, minute, and second formatted according to `TIMESTAMP_FORMAT`
  """
  return dt.datetime.now().strftime(TIMESTAMP_FORMAT)

def ts_print(text: str) -> None:
  """Print text with the formatted time, replacing '%s' with the time"""
  print(text % get_formatted_time())

def replacedt (string: str, replacements: dict, multis: dict = None) -> str:
  """Replace stuff in a string via a dictionary"""
  re_keys = replacements.keys()
  
  if multis:
    for i in multis.keys():
      string = string.replace(str(i), multis[i])
  
  for i in re_keys:
    string = string.replace(str(i), replacements[i])
  return string

def remove (string: str, remove_: str) -> str:
  """Remove a character from a string"""
  return string.replace(remove_, "")

def removelt (string: str, remove_: list) -> str:
  """Remove a list of characters from a string"""
  for i in remove_:
    string = string.replace(i, "")
  return string