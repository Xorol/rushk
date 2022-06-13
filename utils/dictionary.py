import json, interactions, random

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