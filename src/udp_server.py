import socket
import main

DEFAULT_RECEIVE_IP = "0.0.0.0"     
DEFAULT_BROADCAST_IP = "255.255.255.255"
BUFFER_SIZE = 1024

SERVER_PORT=7500
CLIENT_PORT=7501


class UDPServer:
    def __init__(
        self,
        receive_ip=DEFAULT_RECEIVE_IP,
        broadcast_ip=DEFAULT_BROADCAST_IP
    ):
        self.receive_ip = receive_ip
        self.broadcast_ip = broadcast_ip

        # socket for receiving data 
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.bind((self.receive_ip, CLIENT_PORT))

        # socket for broadcasting data
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_BROADCAST,
            1
        )

        print(f"[UDP] Receiving on {self.receive_ip}:{CLIENT_PORT}")
        print(f"[UDP] Broadcasting on {self.broadcast_ip}:{SERVER_PORT}")

    # ==========================
    # Broadcasting
    # ==========================

    def broadcast(self, string):
        self.send_socket.sendto(
            str(string).encode(),
            (self.broadcast_ip, SERVER_PORT)
        )
    
    def announce_game_start(self):
        self.broadcast("201")
        print(f"[UDP] Broadcasted a signal 201, meaning that the game is began")

    # broadcast equipment codes after each player addition
    def broadcast_equipment_id(self, equipment_id):
        self.broadcast(equipment_id)
        print(f"[UDP] Broadcasted equipment ID: {equipment_id}")

    # ==========================
    # Receival
    # ==========================

    def start_readloop(self):
        print("[UDP] started a read-loop")
    
    def end_readloop(self):
        print("[UDP] ended a read-loop")

