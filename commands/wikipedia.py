import interactions, wikipedia, utils

class WikipediaCommands (interactions.Extension):
  def __init__(self, client : interactions.Client):
    self.client = client

  def embedify_page (self, page : wikipedia.WikipediaPage):
    return interactions.Embed(
      title = page.title,
      url = page.url,
      description = page.summary[:550] + "..."
    )

  async def view (self, ctx, kwargs):

    async def check_component (component_ctx : interactions.ComponentContext):
        if int(component_ctx.author.user.id) == int(ctx.author.user.id):
          return True

        await ctx.send("Excuse me, was I asking you?", ephemeral = True)
        return False
      
    page = kwargs["page"]
    
    reses = wikipedia.search(page)

    options = []
    for i in reses:
      options.append(interactions.SelectOption(label = i, value = i))

    _select = interactions.SelectMenu(
      options = options,
      placeholder = "Select the page you'd like",
      custom_id = "page_disambiguation"
    )

    await ctx.send("For precision, select from the dropdown the article you want. Articles can take a bit to load, so be patient", components = _select)
    
    select_ctx : interactions.ComponentContext = await self.client.wait_for_component(
      components = _select,
      check = check_component,
      timeout = 30
    )

    page : wikipedia.WikipediaPage = wikipedia.page(
      title = select_ctx.data.values[0],
      auto_suggest = False,
      preload = True
    )

    await ctx.edit(None, embeds=self.embedify_page(page), components = None)

  async def random(self, ctx : interactions.CommandContext, kwargs):
    try:
      pages = kwargs["pages"]
    except KeyError:
      pages = 1

    if pages == 1:
      await ctx.send(embeds = self.embedify_page(wikipedia.page(wikipedia.random())))
      return

    pages = "Your randomly selected pages are:\n" + "".join([f"> {wikipedia.random()}\n" for _ in range(pages)])
    await ctx.send(pages)

  @interactions.extension_command(
      name = "wikipedia",
      description = "Secret desc lol",
      scope = utils.ids.KOILANG,
      options = [
        interactions.Option(
          name = "view",
          description = "Shows a summary of a Wikipedia page!",
          type = interactions.OptionType.SUB_COMMAND,
          options = [
            interactions.Option(
              name = "page",
              description = "The name of the page to view",
              type = interactions.OptionType.STRING,
              required = True
            )
          ]
        ),
        interactions.Option(
          name = "random",
          description = "Shows a random (or multiple) Wikipedia page(s)!",
          type = interactions.OptionType.SUB_COMMAND,
          options = [
            interactions.Option(
              name = "pages",
              description = "The amount of the pages to see, defaults to 1, max 10.",
              type = interactions.OptionType.INTEGER,
              max_values = 10,
              required = False
            )
          ]
        )
      ]
    )
  async def wikipedia_master_func (self, ctx : interactions.CommandContext, sub_command, **kwargs):
      if sub_command == "view":
        await self.view(ctx, kwargs)
      elif sub_command == "random":
        await self.random(ctx, kwargs)

def setup(client):
  WikipediaCommands(client)