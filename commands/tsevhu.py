import interactions
import utils

class TsevhuCommands(interactions.Extension):
  def __init__(self, client):
    self.client = client

  @interactions.extension_modal("tsevhu_ipa_in")
  async def tsevhu_ipa_in(self, ctx, response):
    await self.tsevhu_to_ipa(ctx, response)

  async def tsevhu_to_ipa_show_modal (self, ctx: interactions.CommandContext):
    text_input = interactions.TextInput(
      style=interactions.TextStyleType.PARAGRAPH,
      label="Enter the text to IPA-ify:",
      custom_id="ipa_input"
    )

    await ctx.popup(interactions.Modal(
      title="Tsevhu to IPA",
      custom_id="tsevhu_ipa_in",
      components=[text_input]
    ))

  async def tsevhu_to_ipa (self, ctx: interactions.CommandContext, response: str):
    response = utils.str.removelt(response, utils.str.PUNCTUATION)
    
    ipa = utils.str.replacedt(
      response, 
      {
        # CONSOS
        "'":"ʔ",
        "j":"ʒ",
        "c":"ç",
        "r":"ɾ",
        "y":"j",
        # VOWELS
        "e":"ɛ"
      },
      {
        # CONSOS
        "kh":"kʰ",
        "tz":"dz",
        "ch":"tʃ",
        "tj":"dʒ",
        "ph":"ɸ",
        "vh":"β",
        "th":"θ",
        "sh":"ʃ",
        "rh":"ɾʰ",
        # VOWELS
        "io":"ijo",
        "ie":"ijɛ",
        "ii":"ɪ",
        "ae":"e",
        "eu":"œ",
        "au":"aʊ",
        "oi":"ɔi",
        "oe":"owɛ",
        "ue":"uwɛ"
      }
    )

    ipa = ipa.rstrip()
    
    await ctx.send("/" + ipa + "/")

  @interactions.extension_command(
    name="tsevhu",
    description="secret desc lol",
    scope=utils.ids.PLAYGROUND,
    options=[
      interactions.Option(
        name="ipa",
        description="Transform your Tsevhu text into IPA!",
        type=interactions.OptionType.SUB_COMMAND
      )
    ]
  )
  async def tsevhu_base (self, ctx: interactions.CommandContext, sub_command, **kwargs):
    if sub_command == "ipa":
      await self.tsevhu_to_ipa_show_modal(ctx)
    
def setup (client):
  TsevhuCommands(client) 
