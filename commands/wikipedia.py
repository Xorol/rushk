import interactions as ipy
import wikipedia
import utils

def get_page(title: str) -> wikipedia.WikipediaPage:
  try:
    page = wikipedia.page(title=title, auto_suggest=False)
  except wikipedia.exceptions.DisambiguationError as e:
    page = wikipedia.page(title=e.options[0], auto_suggest=False)
  return page
  

class WikipediaCommands(ipy.Extension):

  def embedify_page(self, page: wikipedia.page) -> ipy.Embed:
    return ipy.Embed(
      title=page.title,
      url=page.url,
      description=page.summary[:600] + "…",
      thumbnail=page.images[0]
    )
  
  @ipy.slash_command(
    name="wikipedia",
    sub_cmd_name="view",
    sub_cmd_description="View a Wikipedia article"
  )
  @ipy.slash_option(
    description="The name of the page to view",
    required=True,
    opt_type=ipy.OptionType.STRING,
    name="article"
  )
  async def wikipedia_view(self, ctx: ipy.InteractionContext, article: str):
    reses = wikipedia.search(article)

    options = []
    for i in reses:
      options.append(ipy.StringSelectOption(label=i, value=i))

    select = ipy.StringSelectMenu(
      options,
      placeholder = "Select the page you'd like",
      custom_id = "page_disambiguation"
    )

    # define the check
    def check(component) -> bool:
        return component.ctx.author == ctx.author

    message = await ctx.send("Which article do you want to see?", components=select)
    
    try:
        used_select = await self.bot.wait_for_component(components=[select], check=check, timeout=60)
    except TimeoutError:
        select.disabled = True
        await message.edit(components=select)
    else:
        await message.edit(content="", embed=self.embedify_page(get_page(used_select.ctx.values)), components=[])

  @ipy.slash_command(
    name="wikipedia",
    sub_cmd_name="random",
    sub_cmd_description="View a random Wikipedia article"
  )
  async def wikipedia_random(self, ctx: ipy.InteractionContext):
    await ctx.send(embed=self.embedify_page(get_page(wikipedia.random())))

def setup(bot):
  WikipediaCommands(bot)
