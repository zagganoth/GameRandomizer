import random 
from classes import Game

def serialize(session, games):
  session.add_all(games);
  session.commit();


  
def getUnplayed(session):
  return session.query(Game).filter_by(played=False).all();

async def clearPlayed(games, session, channel):
  for game in games:
    game.played = False;
  session.commit()
  await channel.send("All games played. Resetting all to unplayed");
  serialize(session, games);

def rollRandom(games, today):
  random.shuffle(games);
  sumWeights = 0;
  for game in games:
    diffDays = (today - game.lastPlayed).days;
    sumWeights += game.weight + diffDays;
    game.tempWeight = sumWeights;
  result = random.uniform(0, sumWeights);
  print("result is {}".format(result));
  for game in games:
    diffDays = (today - game.lastPlayed).days;
    if(result < (game.tempWeight)):
      return game;   
