from udp_server import UDPServer

class Model:
  def __init__(self, udp_server:UDPServer):
    self.udp=udp_server
  
  def handleInput(self, input: str) -> bool:
    parts = input.split(':')

    if len(parts)!=2 or not parts[0].isdigit() or not parts[1].isdigit() :
      return False
    
    self._handleDigitPair(int(parts[0]), int(parts[1]))
    return True

  # should call methods at self.udp based on the situation
  # TODO: preventing a spaghetti code in collaboration with scores-related features at window.py
  def _handleDigitPair(self, a: int, b: int):
    print("[MODEL]: _handleDigitPair not implemented yet")
