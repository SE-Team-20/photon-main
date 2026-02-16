import socket

DEFAULT_RECEIVE_IP = "0.0.0.0"     
DEFAULT_BROADCAST_IP = "255.255.255.255"
BUFFER_SIZE = 1024


class UDPServer:
    def __init__(
        self,
        receive_ip,
        broadcast_ip
    ):
        self.receive_ip = receive_ip
        self.broadcast_ip = broadcast_ip

        # socket for receiving data 
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.bind((self.receive_ip, 7501))

        # socket for broadcasting data
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_BROADCAST,
            1
        )

        print(f"[UDP] Receiving on {self.receive_ip}:{7501}")
        print(f"[UDP] Broadcasting on {self.broadcast_ip}:{7500}")

    # broadcast equipment codes after each player addition
    def broadcast_equipment_id(self, equipment_id):
        message = str(equipment_id).encode()
        self.send_socket.sendto(
            message,
            (self.broadcast_ip, 7500)
        )
        print(f"[UDP] Broadcasted equipment ID: {equipment_id}")
