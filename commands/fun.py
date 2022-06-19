import interactions, utils

MODE = ""

class FunCommands (interactions.Extension):
  def __init__(self, client):
    self.client = client

  @interactions.extension_command(
    name = "pancak",
    description = "Learn how to make pancaks!",
    scope = utils.ids.PLAYGROUND,
    description_localizations = {
      "es-ES":"Aprende hacer los pancaks!"
    },
  )
  async def pancak (self, ctx : interactions.CommandContext):
    await ctx.send("Paiju:\n\tMud ndu\n\tVi udi oncu\n\tVi hlynna onso, nothii\n\tVi maein oncu\n\tVi nobi onden\n\tQen bu'a onmu\nKveun:\n\tVi'iin, anoavhat wn jima wnd cametu tancam qenmun je.\n\tTan'iin, amiisvhat wn bu'a wnd kiitau yn wnd jima yn.\n\tLeb'iin, ajavhat oajio paijyu syd kiipe yn meq akashvhat.\n\tChas'iin, akpevhat vud zytynyu tanmhai nkor.\n")

  @interactions.extension_command(
    name = "edcypher",
    description = "Encrypt your messages using Ed's Cypher!",
    scope = utils.ids.PLAYGROUND,
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
    scope=utils.ids.PLAYGROUND
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
