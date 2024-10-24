import discord
from command_funcs import read_command
from classes import init
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from queries import getGames, getPlayed
import keep_alive
from secret import secret




engine = create_engine('sqlite:///randomizer.db')
Session = sessionmaker(bind=engine)
session = Session()


client = discord.Client()


@client.event
async def on_message(message):
  if message.author == client.user:
      return
  if message.content.startswith('$hello'):
      await message.channel.send('Hello!')
  if message.content.startswith('?rand '):
      games = getGames(session, message.guild.name) 
      played = getPlayed(session, message.guild.name)
      await read_command(message.content[6:], message.channel, games, played, session)

@client.event
async def on_ready():
  init(engine)
  print('We have logged in as {0.user}'.format(client))


keep_alive.keep_alive()
client.run(secret)

