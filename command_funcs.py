from classes import Game, Command
from utilities import serialize, clearPlayed, rollRandom, getUnplayed
from queries import getPlayed

from datetime import datetime
import re


async def help(args, channel, games, played, session):
  message = ''
  print("Help args: {}".format(args));
  if(args.group(1) != '' and args.group(1) != '\n'):
    message = '\n'.join([command.help for command in commands if command.name in args.group(1).split(" ")]);
  else:
    message = '\n'.join([command.name + ' - ' + command.help for command in commands])
  await channel.send(message);

async def remove(match, channel, games, played, session):
  game = match.group(1);

  for index in range(0,len(games)):
    game_obj = games[index]
    if(game_obj.name == game):
      session.delete(game_obj)
      await channel.send("Removing " + game + " from " + channel.guild.name + "'s list");
      session.commit();
      return
  await channel.send("Could not find " + game + " in your list");

async def setWeight(match, channel, games, played, session):
  game = match.group(1);
  weight = match.group(2);
  game_found = False;
  for game_obj in games:
    if(game_obj.name == game):
      game_obj.weight = weight;
      await channel.send("Successfully updated weight of " + game + " to " + weight);
      game_found = True;
      break;
  if(not(game_found)):
    await channel.send("Could not find " + game + " in your list")

async def unplay(match, channel, games, played, session):
  game = match.group(1);
  for index in range(0,len(played)):
    game_obj = played[index]
    if(game_obj.name == game):
      game_obj.played = False;
      await channel.send("Removing " + game + " from your played games");
      serialize(session, played)
      return
  await channel.send("Could not find " + game + " in your played list");


async def roll(match, channel, games, played, session):
  qualifier = match.group(1);
  today = datetime.now();
  if(qualifier == 'any'):
    game = rollRandom(games, today)
    game.lastPlayed = today;
    game.played = True;
    await channel.send("You should play: " + game.name)
    serialize(session, [game])
    played = getPlayed(session, channel.guild.name);
    if(len(played) == len(games)):
      await clearPlayed(games, session, channel)
  elif(match.group(1) == 'played'):
    if(len(played) == 0):
      await channel.send("No games played! Try rolling a new game with `?rand get new` or `?rand get any`")
    else:
      game = rollRandom(played, today)
      game.lastPlayed = today;
      await channel.send("You should play: " + game.name);
      serialize(session, [game])
  elif(match.group(1) == 'unplayed'):
    unplayed = getUnplayed(session)
    game = rollRandom(unplayed, today)
    game.lastPlayed = today;
    game.played = True;
    await channel.send("You should play: " + game.name)
    serialize(session, [game])
    played = getPlayed(session, channel.guild.name);
    if(len(played) == len(games)):
        await clearPlayed()     
  else:
    await channel.send("Unknown roll command, type `?rand help roll` for options")
async def get(match, channel, games, played, session):
      qualifier = match.group(1);
      today = datetime.now();
      if(qualifier == 'any'):
        game = rollRandom(games, today)
        await channel.send("You should play: " + game.name)
      elif(match.group(1) == 'all'):
        if(len(games) == 0):
          await channel.send("No games added! Try adding some new games with `?rand add <game>`")
        else:
          message = "Here are all the games on {}\n```{:<30} {:<10} {:<45} {:<}\n".format(channel.guild.name,"Name", "Weight", "LastPlayed", "Played") + ''.join([str(game)+"\n" for game in games]) + "```"
          print(message)
          await channel.send(message);
      elif(match.group(1) == 'played'):
        if(len(played) == 0):
          await channel.send("No games played! Try rolling a new game with `?rand get new` or `?rand get any`")
        else:
          message = "Here are all the games played on {}\n```{:<30} {:<10} {:<45} {:<10}\n".format(channel.guild.name, "Name", "Weight", "LastPlayed", "Played") + ''.join([str(game)+"\n" for game in played]) + "```"
          await channel.send(message);
      elif(match.group(1) == 'unplayed'):
        unplayed = getUnplayed(session)
        if(len(unplayed) == 0):
          await clearPlayed();
        await channel.send("Here are all the unplayed games on {}\n```{:<30} {:<10} {:<45} {:<10}\n".format(channel.guild.name,"Name", "Weight", "LastPlayed", "Played") + ''.join([str(game)+"\n" for game in unplayed])) + "```"
      else:
        await channel.send("Unknown get command, type `?rand help get` for options")
           

async def add(match, channel, games, played, session):
    name = match.group(1);
    await channel.send("Adding " + name + " to list for " + channel.guild.name);
    games.append(Game(channel.guild.name, name, 1));
    serialize(session, games)

commands = [Command('add', re.compile(r'add (.*)'), "add <game>", add),
            Command('get', re.compile(r'get (.*)'), "get all|any|played|unplayed", get),
            Command('help', re.compile(r'help(.*)'), "help [cmd]",help),
            Command('remove', re.compile(r'remove (.*)'), 'remove <game>',remove),
            Command('setWeight', re.compile(r"setWeight '(.*)' (.*)"), "setWeight '<game>' <weight>",setWeight),
            Command('unplay', re.compile(r"unplay (.*)"), "unplay <game>",unplay),
            Command('roll', re.compile(r"roll (.*)"), "roll unplayed|any|played", roll)
           ]

async def read_command(command, channel, games, played, session):
    print("Command received: {}".format(command));
    for command_obj in commands:
      if(command_obj.accept(command, channel)):
        await command_obj.process(games, played, session);