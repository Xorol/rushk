import interactions, utils

class IPACommands(interactions.Extension):
  def __init__(self, client : interactions.Client):
    self.client = client

  @interactions.extension_modal("tsevhu_ipa_in")
  async def tsevhu_ipa_in(self, ctx, response):
    response = utils.removelt(response, utils.PUNCTUATION)

    ipa = utils.replacedtck(
      response.lower(), 
      {
        # CONSOS
        "'":"ʔ",
        "j":"ʒ",
        "y":["j", "ə"],
        "w":["w", "ʍu"],
        "k":"k", #kh
        "t":"t", #tz tj th
        "c":"ç", #ch
        "p":"p", #ph
        "v":"v", # vh
        "s":"s", #sh
        "r":"ɾ", # rh
        # VOWELS
        "e":"ɛ", #eu
        "i":"i", #io ie ii
        "a":"a", #ae au
        "o":"o", # oi oe
        "u":"u" # ue
      },
      ck_vars={
        "vowels":["a", "e", "ε","ə", "i", "ɪ", "o", "œ", "ɔ", "u", "ʊ", "y"]
      },
      checks={
        "y":"1 if (i == len(out) - 1) or (next_ not in vowels) else 0",
        "w":"1 if (i == len(out) - 1) or (next_ not in vowels) else 0"
      },
      multis={
        "kh":"kʰ",
        "ch":"tʃ",
        "ph":"ɸ",
        "vh":"β",
        "sh":"ʃ",
        "rh":"ɾʰ",
        "th":"θ",
        "tz":"dz",
        "tj":"dʒ",
        "eu":"œ",
        "io":"ijo",
        "ie":"ijε",
        "ii":"ɪ",
        "ae":"e",
        "au":"aʊ",
        "oi":"ɔi",
        "oe":"owε",
        "ue":"uwε"
      },
      unchanged=[
        "b", "d", "g", "q", "f", "m", "w", "n", "x", "h", "l", "z"
      ]
    )

    ipa = ipa.rstrip()

    await ctx.send(f"/{ipa}/")

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

  @interactions.extension_modal("ciscun_ipa_in")
  async def ciscun_to_ipa(self, ctx, response):
    response = utils.removelt(response, utils.PUNCTUATION)

    response = utils.replacedtck(
      response.lower(),
      {
        "p":"ʘ",
        "f":"ɸ",
        "h":"x",
        "c":"k",
        "s":"s",
        "n":["n", "ŋ"]
      },
      multis={
        "sh":"ʃ"
      },
      unchanged=[
        "i", "a", "u"
      ],
      ck_vars={
        "vowels":['i', 'a', 'u']
      },
      checks={
        "n":"1 if next_ in vowels else 0",
      }
    ).rstrip()

    await ctx.send(f"/{response}/")
    
  async def ciscun_to_ipa_show_modal (self, ctx: interactions.CommandContext):
    text_input = interactions.TextInput(
      style=interactions.TextStyleType.PARAGRAPH,
      label="Enter the text to IPA-ify:",
      custom_id="ipa_input"
    )

    await ctx.popup(interactions.Modal(
      title="Ciscun to IPA",
      custom_id="ciscun_ipa_in",
      components=[text_input]
    ))

  @interactions.extension_modal("gedenano_ipa_in")
  async def gedenano_to_ipa(self, ctx, response):
    response = utils.removelt(response, utils.PUNCTUATION)
    ipa = utils.replacedtck(
      response.lower(),
      {
        "c":"k",
        "e":"ε",
        "a":"ɑ",
        "á":"ɑ:",
        "é":"ε:",
        "í":"i:",
        "ó":"o",
        "ú":"u:",
        "v":["v", "f"]
      },
      multis={
        "gn":"ŋ",
        "aj":"ɑi",
        "oj":"oi"
      },
      checks={
        "v":"0 if (i != len(out) - 1) or ( next_ != ' ') else 1"
      },
      unchanged=[
        "b", "p", "d", "t", "z", "s", "m", "n", "r", "g", "i", "o", "u", "j"
      ]
    ).rstrip()
    await ctx.send(f"/{ipa}/")

  @interactions.extension_command(
    name="ipa",
    description="Transform clong text into IPA!",
    scope=utils.KOILANG,
    options=[
      interactions.Option(
        name="language",
        type=interactions.OptionType.STRING,
        description="The language to interpret the text in",
        required=True,
        choices=[
          interactions.Choice(name="Tsevhu",value="tsevhu"),
          interactions.Choice(name="Ciscun",value="ciscun")
        ]
      )
    ]
  )
  async def ipa(self, ctx, language):
    if language == "tsevhu":
      await self.tsevhu_to_ipa_show_modal(ctx)
    elif language == "ciscun":
      await self.ciscun_to_ipa_show_modal(ctx)

def setup(client):
  IPACommands(client)
