import interactions
from .ids import KOILANG_CHANNEL_IDS

async def set_game(game : str, client : interactions.Client):
  await client.change_presence(interactions.ClientPresence(activities=[interactions.PresenceActivity(name=game, type=interactions.PresenceActivityType.GAME)]))

async def get_user (id : int, client : interactions.Client):
  return interactions.User(**await client._http.get_user(id), _client=client._http)

async def get_channel(client : interactions.Client, channel_name : str):
  """
  Creates a channel object correspoding to `channel_name`, to which messages can be sent and stuff
  """
  
  return interactions.Channel( # turns it into a channel object
    ** await client._http.get_channel(KOILANG_CHANNEL_IDS[channel_name]), # Gets the channel
    _client = client._http
  )