from interface import Server
from database import Database

# 
# core purpose: handling data between a server and clients
# 
class Model:
  GREEN = 0
  RED = 1

  def __init__(self, server:Server, database:Database):
    self.udp=server
    self.db=database
    self.basedq = []
    self.basedset = set()
  
  # called every frame by window.py
  def popBasedPlayerID(self):
    if len(self.basedq)==0:
      return False
    return self.basedq[0]

  # this will be called by self.handleInput()
  def _insertBasedPlayerID(self, id):
    if self.basedset in id:
      return
    self.basedset.add(id)
    self.basedq.append(id)

  #  called by UDPServer in need
  def handleInput(self, input: str) -> bool:
    parts = input.split(':')

    if len(parts)!=2 or not parts[0].isdigit() or not parts[1].isdigit() :
      return False
    
    self._handleDigitPair(int(parts[0]), int(parts[1]))
    return True
  
  # TODO: fix this
  # return a value exactly how it's stored in the database class
  def _getPlayerID(self, equip_id: int) -> int:
    return 0
  
  # TODO: fix this
  # return either 0 or 1 (red or green)
  def _getTeamID(self, equip_id: int) -> int:
    return equip_id%2

  # TODO: fix this
  # should be stored permanently / reflected on the leaderboard
  def _grantScore(self, player_id: int, diff: int) -> bool:
    return False

  # should call methods at self.udp based on the situation
  # TODO: add some logics and turn this viable
  def _handleDigitPair(self, a: int, b: int):
    print("[MODEL]: _handleDigitPair not implemented yet")

    playerA=self._getPlayerID(a)
    
    # base event
    if(b in ["43", "53"]):
      playerA = self._getPlayerID(a)
      if(b=="43" and RED==self._getTeamID(playerA) or a=="53" and GREEN==self._getTeamID(playerA)):
        self._insertBasedPlayerID(playerA)
        self._grantScore(playerA, 100)
      return
    
    # pvp event
    playerB=self._getPlayerID(b)

    #TODO: do something
    