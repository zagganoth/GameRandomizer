from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


Base = declarative_base()
class Game(Base):
  __tablename__ = 'game'
  name = Column(String(50), primary_key=True)
  guild = Column(String(50), primary_key=True)
  weight = Column(Integer)
  lastPlayed = Column(DateTime)
  played = Column(Boolean)

  def __init__(self, guild, name, weight, lastPlayed=None):
    self.guild = guild
    self.name = name;
    self.weight = weight;
    self.tempWeight = 0;
    if(lastPlayed is not None):
      self.lastPlayed = lastPlayed;
    else:
      self.lastPlayed = datetime.now();
    self.played = False
  def __str__(self):
    return "{:<30} {:<10} {:<45} {:<10}".format(self.name, self.weight, self.lastPlayed.strftime("%Y-%m-%d %H:%M:%S.%f"), str(self.played))
  def __repr__(self):
    return self.__str__();

class Command:
  def __init__(self, name, regex, help, func):
    self.name = name;
    self.help = help;
    self.regex = regex;
    self.func = func;
    self.match = None;
    self.channel = None;
  def accept(self, command, channel):
    self.match = self.regex.match(command)
    self.channel = channel;
    return self.match is not None;
  async def process(self, games, played, session):
    await self.func(self.match, self.channel, games, played, session);
  def __repr__(self):
    return "name: {}, help: {}, regex: {}, func: {}, match: {}".format(self.name, self.help, self.regex, self.func,self.match);
def init(engine):
  Base.metadata.create_all(engine)
