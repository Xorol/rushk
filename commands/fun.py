import interactions, utils

class FunCommands (interactions.Extension):
  def __init__(self, client):
    self.client = client

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
      ),
      interactions.Option(
        name = "text",
        description = "The text to en/decrypt",
        type = interactions.OptionType.STRING,
        required = True
      ),
      interactions.Option(
        name = "key",
        description = "The key for the cypher",
        type = interactions.OptionType.STRING,
        required = True
      ),
      interactions.Option(
        name = "offset",
        description = "The amount by which to offset the output",
        type = interactions.OptionType.INTEGER,
        required = True
      )
    ]
  )
  async def edcypher(self, ctx : interactions.CommandContext, mode : str, text : str, key : str, offset : int):
    text = [ord(i) for i in text]
    key = [ord(i) * key.count(i) for i in key]

    out = []
    if mode == "encrypt":
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