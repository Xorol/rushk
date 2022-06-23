import interactions, utils, datetime

MODE = ""

class FunCommands (interactions.Extension):
  def __init__(self, client):
    self.client = client
  
  @interactions.extension_command(
    name="format-time",
    scope=utils.ids.KOILANG,
    description="Format time",
    options=[
      interactions.Option(
        name="day",
        description="The day of the date to format",
        type=interactions.OptionType.INTEGER,
        required=True,
        min_values=1,
        max_values=31
      ),
      interactions.Option(
        name="month",
        description="The month of the date to format",
        required=True,
        type=interactions.OptionType.INTEGER,
        choices=[
          interactions.Choice(name="January",value=1),
          interactions.Choice(name="February",value=2),
          interactions.Choice(name="March",value=3),
          interactions.Choice(name="April",value=4),
          interactions.Choice(name="May",value=5),
          interactions.Choice(name="June",value=6),
          interactions.Choice(name="July",value=7),
          interactions.Choice(name="August",value=8),
          interactions.Choice(name="September",value=9),
          interactions.Choice(name="October",value=10),
          interactions.Choice(name="November",value=11),
          interactions.Choice(name="December",value=12),
        ]
      ),
      interactions.Option(
        name="year",
        description="The year of the date to format",
        required=True,
        type=interactions.OptionType.INTEGER,
        min_values=0,
      ),
      interactions.Option(
        name="format",
        description="The format of the timestamp",
        type=interactions.OptionType.STRING,
        required=True,
        choices=[
          interactions.Choice(name="Short time (HH:MM PM/AM)", value="t"),
          interactions.Choice(name="Long time (HH:MM:SS PM/AM)", value="T"),
          interactions.Choice(name="Short date (DD/MM/YYYY)", value="d"),
          interactions.Choice(name="Long date (DD month YYYY)", value="D"),
          interactions.Choice(name="Short datetime (DD month YYYY HH:MM AM/PM)", value="f"),
          interactions.Choice(name="Long datetime (day DD month YYYY HH:MM AM/PM)", value="F"),
          interactions.Choice(name="Relative time (two months ago)", value="R"),
        ]
      ),
      interactions.Option(
        name="hour",
        description="MUST BE 24-HOUR",
        type=interactions.OptionType.INTEGER,
        required=False,
        min_values=0,
        max_values=24
      ),
      interactions.Option(
        name="minute",
        description="The minute of the date to format",
        type=interactions.OptionType.INTEGER,
        required=False,
        min_values=0,
        max_values=60
      ),
      interactions.Option(
        name="second",
        description="The second of the date to format",
        type=interactions.OptionType.INTEGER,
        required=False,
        min_values=0,
        max_values=60
      )
    ]
  )
  async def format_time(self, ctx, day: int, month: int, year: int, format: str, hour:int = 0, minute:int = 0, second:int = 0):
    dt = datetime.datetime(year, month, day, hour, minute, second)
    embedu = interactions.Embed(
      title="Time format",
      fields=[
        interactions.EmbedField(name="Preview", value=f"<t:{int(dt.timestamp())}:{format}>", inline=True),
        interactions.EmbedField(name="Plain text", value=f"`<t:{int(dt.timestamp())}:{format}>`", inline=True)
      ]
    )
    await ctx.send(embeds=embedu)

  @interactions.extension_command(
    name = "pancak",
    description = "Learn how to make pancaks!",
    scope = utils.ids.KOILANG,
    description_localizations = {
      "es-ES":"Aprende hacer los pancaks!"
    },
  )
  async def pancak (self, ctx : interactions.CommandContext):
    await ctx.send("Paiju:\n\tMud ndu\n\tVi udi oncu\n\tVi hlynna onso, nothii\n\tVi maein oncu\n\tVi nobi onden\n\tQen bu'a onmu\nKveun:\n\tVi'iin, anoavhat wn jima wnd cametu tancam qenmun je.\n\tTan'iin, amiisvhat wn bu'a wnd kiitau yn wnd jima yn.\n\tLeb'iin, ajavhat oajio paijyu syd kiipe yn meq akashvhat.\n\tChas'iin, akpevhat vud zytynyu tanmhai nkor.\n")

  @interactions.extension_command(
    name = "edcypher",
    description = "Encrypt your messages using Ed's Cypher!",
    scope = utils.ids.KOILANG,
    options = [
      interactions.Option(
        name = "mode",
        type = interactions.OptionType.STRING,
        description = "Tells the bot whether to encrypt or decrypt",
        required = True,
        choices = [
          interactions.Choice(
            name = "Encrypt",
            value = "encrypt"
          ),
          interactions.Choice(
            name = "Decrypt",
            value = "decrypt"
          )
        ]
      )
    ]
  )
  async def edcypher(self, ctx : interactions.CommandContext, mode: str):
    text = interactions.TextInput(
      style=interactions.TextStyleType.PARAGRAPH,
      label="Enter the text to en/decrypt:",
      custom_id="beezchurger"
    )
    key = interactions.TextInput(
      style=interactions.TextStyleType.SHORT,
      label="Enter the key:",
      custom_id="llave"
    )
    offset = interactions.TextInput(
      style=interactions.TextStyleType.SHORT,
      label="Enter the number by which to offset:",
      custom_id="offset"
    )
    
    global MODE
    MODE = mode

    await ctx.popup(interactions.Modal(
      title="Ed's Cypher",
      custom_id="edcypher",
      components=[text, key, offset]
    ))

  @interactions.extension_modal("edcypher")
  async def do_cypher(self, ctx: interactions.CommandContext, text: str, key: str, offset: str):
    text = [ord(i) for i in text]
    key = [ord(i) * key.count(i) for i in key]

    try:
      offset = int(offset)
    except ValueError:
      await ctx.send("Your offset must be a number!", ephemeral=True)
      return

    out = []
    
    global MODE
    if MODE == "encrypt":
        for i, j in enumerate(text):
            out.append(chr(j + key[i % len(key)] + offset))
    else:
      for i, j in enumerate(text):
          out.append(chr(j - key[i % len(key)] - offset))
    out = ''.join(out)
    await ctx.send(out)

  @interactions.extension_command(
    name = "no",
    description="You don't want to do this...",
    scope=utils.ids.KOILANG
  )
  async def no (self, ctx: interactions.CommandContext):
    with open("commands/no.txt") as f:
      lines = f.readlines()

    lines[0] = str(int(lines[0]) + 1)

    await ctx.send(f"You have unleashed the no!\nYou are victim no.: {lines[0]}")

    with open("commands/no.txt", "w") as f:
      f.write("".join(lines))
    
    for i in lines[1:]:
      await ctx.author.send(i)

def setup (client):
  FunCommands(client)
