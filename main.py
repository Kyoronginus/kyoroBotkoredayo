import discord

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {@.user}.format(client)')

  @Client.event
  async def on_message(message):
    if message.author == client.user:
      return

    if message.content.starswith('$hello'):
      await message.channel.send('Hello!')

client.run()