from classes import Game

def getPlayed(session, guild):
  return session.query(Game).filter_by(guild=guild,played=True).all()

def getGames(session, guild):
  return session.query(Game).filter_by(guild=guild).all()