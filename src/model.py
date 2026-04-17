from interface import Server
from collections import deque
import database

# 
# core purpose: handling data between a server and clients
# 
class Model:
  GREEN = 0
  RED = 1

  def __init__(self, server:Server):
    self.udp=server
    self.basedq = deque()
    self.basedset = set()
    self.messageq = deque()
    self.scorediffq = deque()
    self.equip_to_codename = {} # codename dictionary via equip id

  # def basedPlayerCount(self):
  #   return len(self.basedq)
  
  def pop_live_message(self):
    return self.messageq.popleft() if self.messageq else False
  
  # called every frame by window.py
  def pop_based_equip_id(self):
    return self.basedq.popleft() if self.basedq else False

  def pop_score_diff(self):
    return self.scorediffq.popleft() if self.scorediffq else False

  # this will be called by self.handleInput()
  def _insertBasedEquipID(self, id):
    if id in self.basedset:
      return
    self.basedset.add(id)
    self.basedq.append(id)
  
  def _insertLiveMessage(self, string:str, emergent=False):
    if emergent:
      self.messageq.appendleft(string)
    else:
      self.messageq.append(string)

  #  called by UDPServer in need
  def handleInput(self, input: str) -> bool:
    parts = input.split(':')
    print(f"[Model] handleInput called with: {input}")

    if len(parts)!=2 or not parts[0].isdigit() or not parts[1].isdigit() :
      return False
    
    self._handleDigitPair(int(parts[0]), int(parts[1]))
    return True
  
  # TODO: needs to implemented
  # return a value exactly how it's stored in the database class
  # def _getPlayerID(self, equip_id: int) -> int:
  #   return 0
  
  # # TODO: needs to be implemented
  # # return either 0 or 1 (red or green)
  # def _getTeamID(self, equip_id: int) -> int:
  #   return equip_id%2

  def _grant_score(self, equip_id: int, diff: int):
    self.scorediffq.append((equip_id, diff))

  # should call methods at self.udp based on the situation
  def _handleDigitPair(self, hitter: int, receiver: int):
    print(f"[Model] _handleDigitPair: hitter={hitter}, receiver={receiver}")
    print(f"[Model] equip_to_codename: {self.equip_to_codename}")
    hitter_name = self.equip_to_codename.get(hitter)
    receiver_name = self.equip_to_codename.get(receiver)

    if hitter_name is None or receiver_name is None:
      print(f"Unknown equipment ID(s): hitter={hitter}, receiver={receiver}")
      return

    self._grant_score(hitter, 10)
    self._insertLiveMessage(f"{hitter_name} hit {receiver_name}")

    
  #   # base event
  #   if(b in ["43", "53"]):
  #     if(b=="43" and RED==self._getTeamID(equipA) or a=="53" and GREEN==self._getTeamID(equipA)):
  #       self._insertBasedEquipID(equipA)
  #       self._grant_score(equipA, 100)
  #     return
    
  #   # pvp event
  #   equipB=b

  #   if self._getTeamID(equipA) != self._getTeamID(equipB):
  #     # TODO: stun playerB on hit
  #     # TODO: grant score to playerA
  #     print("normal combat not implemented")
  #   else:
  #     # TODO: do NOT stun playerB (or as an instruction specifies)
  #     # TODO: grant penalty to playerA
  #     #TODO: call udp server to do something
  #     print("handling friendly fire not implemented")
