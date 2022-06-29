import interactions, utils

class LanguageCommands (interactions.Extension):
  def __init__(self, client : interactions.Client):
    self.client = client

  @interactions.extension_command(
    name = "hsilgne",
    description = "Translates your text in or out of hsilgnE!",
    scope = utils.KOILANG,
    options = [
      interactions.Option(
        name = "language",
        description = "The translation language",
        type = interactions.OptionType.STRING,
        required = True,
        choices = [
          interactions.Choice(name = "Translate to English", value = "english"),
          interactions.Choice(name = "Translate to hsilgnE", value = "hsilgne")
        ]
      ),
      interactions.Option(
        name = "text",
        description = "The text to translate",
        type = interactions.OptionType.STRING,
        required = True
      )
    ]
  )
  async def hsilgne (self, ctx : interactions.CommandContext, language : str, text : str):
    dest = "English" if language == "english" else "hsilgnE"
    orig = "hsilgnE" if language == "english" else "English"
    
    embedo = interactions.Embed(
      title = "Translation",
      fields = [
        interactions.EmbedField(name = orig, value = text),
        interactions.EmbedField(name = dest, value = text[::-1])
      ]
    )
    
    await ctx.send(embeds = embedo)
    
def setup (client):
  LanguageCommands(client)