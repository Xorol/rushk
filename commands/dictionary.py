import interactions, random, json, utils

dictionary_choices = utils.generate_dictionary_choices()

class DictionaryCommands (interactions.Extension):
  def __init__(self, client):
    self.client : interactions.Client = client

  async def search (self, ctx : interactions.CommandContext, args : dict):
    dict = utils.Dictionary(args['dictionary'], utils.load_dictionaries())
    res = dict.search(args['term'], args['specificity'])

    if len(res) >= 2000:    
      await ctx.send("Your search was too broad, I shall unleash koifire unto your DMs, banashing them to hell!")
      k2 = 2000
      res = [res[i:i+k2] for i in range(0, len(res), k2)]
      for i in res:
        await ctx.author.send(res)
      return
      
    if len(res) > 300:
      await ctx.author.send(res)
      await ctx.send("Your search was too broad, I will now unleash koifire unto your DMs, banishing them to hell")
      return

    await ctx.send(res)

  async def random(self, ctx : interactions.CommandContext, args : dict):
    dicts = utils.load_dictionaries()
    if args["dictionary"] == "random_dict":
      names = list(dicts.keys())
      dict = utils.Dictionary(random.choice(names), dicts)
    else:
      dict = utils.Dictionary(args['dictionary'], dicts)

    await ctx.send(f"A random word from {dict.display_name}:\n{dict.random_word()}")

  async def info(self, ctx : interactions.CommandContext, args : dict):
    dicty = utils.Dictionary(args['dictionary'], utils.load_dictionaries())
    embeda = interactions.Embed(
        title=dicty.display_name,
        description=dicty.description or "Placeholder...",
        url=dicty.link or None,
        thumbnail=interactions.EmbedImageStruct(
            url=dicty.image)._json if dicty.image else None,
        fields=[
            interactions.EmbedField(
                name="Owner",
                value=f"{dicty.owner['name']}#{dicty.owner['discriminator']}",
            ),
            interactions.EmbedField(name="Words", value=len(dicty.words)),
            interactions.EmbedField(
                name="Sample Word", value=dicty.random_word()),
        ],
    )

    await ctx.send(embeds=embeda)

  @interactions.extension_command(
    name = "dictionary",
    description = "Secret desc lol",
    scope = utils.KOILANG,
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
            required = False,
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
                required=False,
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
      )
    ]
  )
  async def dictionary (self, ctx : interactions.CommandContext, sub_command : str, **kwargs):
    match sub_command:
      case "search":
        try:
          _ = kwargs['specificity']
        except KeyError:
          kwargs['specificity'] = "broad"
          
        await self.search(ctx, kwargs)
      case "random":
        try:
          _ = kwargs['dictionary']
        except KeyError:
          kwargs['dictionary'] = "random_dict"
        await self.random(ctx, kwargs)
      case "info":
        await self.info(ctx, kwargs)

def setup (client):
  DictionaryCommands(client)
