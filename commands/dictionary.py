import interactions as ipy
from interactions.ext.paginators import Paginator
import asyncio
import utils
import random
from typing import Annotated


class DictionaryConverter(ipy.Converter):
  async def convert(ctx, argument: str):
    if argument == "all" or argument == "random":
      return argument
    return utils.Dictionary(argument, utils.load_dictionaries())

class DictionaryCommands(ipy.Extension):
  @ipy.slash_command(
    name="dictionary", 
    sub_cmd_name="guess-the-language", 
    sub_cmd_description="Guess what language a word's from!", 
    scopes=[986960242325729300]
  )
  async def guess_the_language(self, ctx: ipy.InteractionContext):
      dictionary_obj = utils.random_dictionary()
      dictionaries = utils.load_dictionaries()
      dictionaryselect = ipy.StringSelectMenu(*[dictionaries[i]["display"] for i in dictionaries],)
      message = await ctx.send(f"What language is this word from?\n{dictionary_obj.random_word()}", components=dictionaryselect)
  
      def check(component):
        return component.ctx.author == ctx.author
  
      try:
        used_component = await self.bot.wait_for_component(components=dictionaryselect, check=check, timeout=30)
      except asyncio.exceptions.TimeoutError:
          dictionaryselect.disabled = True
          await message.edit(components=dictionaryselect)
      else:
          if used_component.ctx.values[0] == dictionary_obj.display_name:
            await message.edit(content=f"{message.content}\n\n{dictionary_obj.display_name} is correct!")
          else:
            await message.edit(f"{message.content}\n\nNope! It was {dictionary_obj.display_name}")
          dictionaryselect.disabled = True
          await message.edit(components=dictionaryselect)

  @ipy.slash_command(
    name="dictionary",
    sub_cmd_name="search",
    sub_cmd_description="Search a dictionary!",
    scopes=[986960242325729300]
  )
  @ipy.slash_option(
    name="dictionary",
    description="The dictionary to use",
    opt_type=ipy.OptionType.STRING,
    required=True,
    choices=[ipy.SlashCommandChoice(name=i["display"], value=i["name"]) for i in utils.load_dictionaries().values()] + [ipy.SlashCommandChoice(name="All dictionaries", value="all")]
  )
  @ipy.slash_option(
    name="term",
    description="The term to search for",
    required=True,
    opt_type=ipy.OptionType.STRING
  )
  @ipy.slash_option(
    name="specificity",
    description="If set to narrow, only shows results that are the item; If broad, shows results that contain it",
    required=False,
    opt_type=ipy.OptionType.STRING,
    choices=[
        ipy.SlashCommandChoice(name="Broad", value='broad'),
        ipy.SlashCommandChoice(name="Narrow", value="narrow")
    ]
  )
  async def search (self, ctx: ipy.InteractionContext, dictionary: DictionaryConverter, term: str, specificity: str = "broad"):
    if dictionary == "all":
      dictionaries = utils.load_dictionaries()
      res = []
      for i in dictionaries.values():
        results = utils.Dictionary(i["name"], dictionaries).search(term, specificity, blocks=True)
        if "No results" not in results:
          res += results
    else:
      res = dictionary.search(term, specificity)
    if dictionary == "all":
      paginator = utils.WordPaginator.create_from_blocks(self.client, res)
      try:
        await paginator.send(ctx)
        return
      except:
        return
    if len(res) > 500:
      res = dictionary.search(term, specificity, blocks=True)
      paginator = utils.WordPaginator.create_from_blocks(self.client, res)
      await paginator.send(ctx)
    else:
      await ctx.send(res)

  @ipy.slash_command(
    name="dictionary",
    sub_cmd_name="random",
    sub_cmd_description="Get a random word stored in Rushk!",
    scopes=[986960242325729300]
  )
  @ipy.slash_option(
    name="dictionary",
    description="The dictionary to get a random word from",
    opt_type=ipy.OptionType.STRING,
    required=False,
    choices=[ipy.SlashCommandChoice(name=i["display"], value=i["name"]) for i in utils.load_dictionaries().values()] + [ipy.SlashCommandChoice(name="Random dictionary", value="random")]
  )
  async def random_word(self, ctx: ipy.InteractionContext, dictionary: DictionaryConverter = "random"):
    if dictionary == "random":
      dictionary = utils.random_dictionary()
    await ctx.send(f"### A random word from {dictionary.display_name}\n" + dictionary.random_word())

  @ipy.slash_command(
    name="dictionary",
    sub_cmd_name="info",
    sub_cmd_description="Find out more about any dictionary!",
    scopes=[986960242325729300]
  )
  @ipy.slash_option(
    name="dictionary",
    description="The dictionary to find out about",
    opt_type=ipy.OptionType.STRING,
    required=True,
    choices=[ipy.SlashCommandChoice(name=i["display"], value=i["name"]) for i in utils.load_dictionaries().values()]
  )
  async def info(self, ctx: ipy.InteractionContext, dictionary: DictionaryConverter):
    embed = ipy.Embed(
      title=dictionary.display_name,
      description=dictionary.description,
      url=dictionary.link,
      fields=[
        ipy.EmbedField(name="Owner", value=f"<@{dictionary.owner_id}>", inline=True),
        ipy.EmbedField(name="Length", value=f"{dictionary.length} words", inline=True),
        ipy.EmbedField(name="Sample word", value=dictionary.random_word(), inline=True)
      ],
      thumbnail=dictionary.image
    )
    await ctx.send(embeds=embed, allowed_mentions=ipy.AllowedMentions.none())

    
    
def setup(bot):
  DictionaryCommands(bot)
