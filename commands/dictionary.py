import interactions, random, json, utils

dictionary_choices = utils.dictionary.generate_dictionary_choices()

class DictionaryCommands (interactions.Extension):
  def __init__(self, client):
    self.client : interactions.Client = client

  async def search (self, ctx : interactions.CommandContext, args : dict):
    dict = utils.dictionary.Dictionary(args['dictionary'], utils.dictionary.load_dictionaries())
    res = dict.search(args['term'], args['specificity'])

    if len(res) >= 2000:
      # The amount pf words in one message
      a = 5 * 2
      
      r = res.split("\n", a)[a]
      for i in res[:-len(r) - 1]:
        await ctx.send("Your search was too broad, I will now unleash koifire unto your DMs, banishing them to hell")
        await ctx.author.send(i)
      return
      
    if len(res) > 300:
      await ctx.author.send(res)
      await ctx.send("Your search was too broad, I will now unleash koifire unto your DMs, banishing them to hell")
      return

    await ctx.send(res)

  async def random(self, ctx : interactions.CommandContext, args : dict):
    dicts = utils.dictionary.load_dictionaries()
    if args["dictionary"] == "random_dict":
      names = list(dicts.keys())
      dict = utils.dictionary.Dictionary(random.choice(names), dicts)
    else:
      dict = utils.dictionary.Dictionary(args['dictionary'], dicts)

    await ctx.send(f"A random word from {dict.display_name}:\n{dict.random_word()}")

  async def info(self, ctx : interactions.CommandContext, args : dict):
    dict = utils.dictionary.Dictionary(args['dictionary'], utils.dictionary.load_dictionaries())
    embeda = interactions.Embed(
      title = dict.display_name,
      description = dict.description if dict.description else "Placeholder...",
      url = dict.link if dict.link else None,
      thumbnail = interactions.EmbedImageStruct(url=dict.image)._json if dict.image else None,
      fields = [
        interactions.EmbedField(name = "Owner", value=f"{dict.owner['name']}#{dict.owner['discriminator']}"),
        interactions.EmbedField(name="Words", value = len(dict.words)),
        interactions.EmbedField(name="Sample Word", value=dict.random_word())
      ]
    )
    
    await ctx.send(embeds=embeda)

  async def edit (self, ctx : interactions.CommandContext, args : dict):
    dict = utils.dictionary.Dictionary(args['dictionary'], utils.dictionary.load_dictionaries())
    
    if ctx.user.username != dict.owner["name"] or ctx.user.discriminator != dict.owner["discriminator"]:
      await ctx.send("You can't edit that! It's not yours!")
      return

    json_dicts = utils.dictionary.load_dictionaries()

    item = args["item"]
    new = args["new"]

    json_dicts[dict.name][item] = new

    with open("dictionaries/dictionaries.json", "w") as f:
      json.dump(json_dicts, f)

    if item == "display":
      await ctx.send("Your dictionary's name has been updated, but it will not show in the commands until I'm reloaded!")
      return

    await ctx.send("Your dictionary has been updated!")
    

  @interactions.extension_command(
    name = "dictionary",
    description = "Secret desc lol",
    scope = utils.ids.KOILANG,
    options = [
      interactions.Option(
        name = "search",
        description = "Search a dictionary!",
        type = interactions.OptionType.SUB_COMMAND,
        options = [
          interactions.Option(
            name="dictionary",
            description="The dictionary to search",
            type = interactions.OptionType.STRING,
            required=True,
            choices=dictionary_choices,
          ),
          interactions.Option(
            name = "term",
            description = "The term to search for",
            type = interactions.OptionType.STRING,
            required = True,
          ),
          interactions.Option(
            name = "specificity",
            description = "If set to narrow, only shows results that are the item; If broad, shows results that contain it.",
            type = interactions.OptionType.STRING,
            required = True,
            choices = [
              interactions.Choice(name = "Broad search", value = "broad"),
              interactions.Choice(name = "Narrow search", value = "narrow")
            ]
          )
        ]
      ),
      interactions.Option(
            name = "random",
            description = "Gets a random word from a chosen dictionary!",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
              interactions.Option(
                name="dictionary",
                description="The dictionary to get a random word from",
                type = interactions.OptionType.STRING,
                required=True,
                choices=dictionary_choices + [interactions.Choice(name="Random dictionary", value="random_dict")],
              )
            ]
          ),
      interactions.Option(
        name = "info",
        description = "Get info about a dictionary",
        type = interactions.OptionType.SUB_COMMAND,
        options = [
          interactions.Option(
            name = "dictionary",
            description="The dictionary to get info about",
            type = interactions.OptionType.STRING,
            required = True,
            choices = dictionary_choices
          )
        ]
      ),
      interactions.Option(
        name = "edit",
        description = "Edit your dictionary!",
        type = interactions.OptionType.SUB_COMMAND,
        options = [
          interactions.Option(
            name = "dictionary",
            description="The dictionary to edit",
            type = interactions.OptionType.STRING,
            required = True,
            choices = dictionary_choices
          ),
          interactions.Option(
                name="item",
                description="The thing to edit",
                type = interactions.OptionType.STRING,
                required=True,
                choices=[
                  interactions.Choice(name = "Image", value="image"),
                  interactions.Choice(name = "Dictionary Link", value="dictionary"),
                  interactions.Choice(name = "Name", value="display"),
                  interactions.Choice(name = "Description", value="description"),
                ]
            ),
            interactions.Option(
              name = "new",
              description="What to replace the item with",
              type = interactions.OptionType.STRING,
              required = True
            ),
          ]
        )
      ]
  )
  async def dictionary (self, ctx : interactions.CommandContext, sub_command : str, **kwargs):
    if sub_command == "search":
      await self.search(ctx, kwargs)
    elif sub_command == "random":
      await self.random(ctx, kwargs)
    elif sub_command == "info":
      await self.info(ctx, kwargs)
    elif sub_command == "edit":
      await self.edit(ctx, kwargs)

def setup (client):
  DictionaryCommands(client)