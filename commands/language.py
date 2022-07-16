import interactions, utils, translators as tr
from iso639 import to_name

class LanguageCommands (interactions.Extension):
  def __init__(self, client : interactions.Client):
    self.client = client
   
  @interactions.extension_message_command(
    name="Translate",
    scope=utils.KOILANG
  )
  async def translate_command(self, ctx: interactions.CommandContext):
    content = str(ctx.target)

    translated_lang = to_name(tr.google(content, is_detail_result=True)[-1])
    translated = tr.google(content)

    embedse = interactions.Embed(
      title="Translation",
      fields=[
        interactions.EmbedField(name="Original text", value=content, inline=True),
        interactions.EmbedField(name="Translated text", value=translated, inline=True),
        interactions.EmbedField(name="Detected language", value=translated_lang, inline=True)
      ]
    )
    await ctx.send(embeds=embedse, ephemeral=True)

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
