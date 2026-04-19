import socket
import random
import time

from util import isDevMode

BUFFER_SIZE = 1024
SERVER_ADDR = ("0.0.0.0", 7500)
CLIENT_ADDR = ("127.0.0.1", 7501)

CODE_GAME_START = "202"
CODE_GAME_END = "221"
BASE_GREEN = "43"
BASE_RED = "53"

if isDevMode():
    red_players = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
    green_players = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
else:
    print("[TG] Enter equipment IDs for RED team (odd numbers, up to 15 players).")
    print("[TG] Press Enter to stop adding players.\n")
    red_players = []
    for i in range(1, 16):
        val = input(f"[TG] Red player {i} equipment ID (or Enter to stop): ").strip()
        if not val:
            break
        red_players.append(int(val))

    print("\n[TG] Enter equipment IDs for GREEN team (even numbers, up to 15 players).")
    print("[TG] Press Enter to stop adding players.\n")
    green_players = []
    for i in range(1, 16):
        val = input(f"[TG] Green player {i} equipment ID (or Enter to stop): ").strip()
        if not val:
            break
        green_players.append(int(val))

if not red_players or not green_players:
    print("[TG] Error: at least 1 player per team required.")
    exit(1)

print(f"\n[TG] Red team  ({len(red_players)} players): {red_players}")
print(f"[TG] Green team ({len(green_players)} players): {green_players}")

recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_sock.bind(SERVER_ADDR)

print("\n[TG] Waiting for game start signal from main.py...")
data = ""
while data != CODE_GAME_START:
    data, _ = recv_sock.recvfrom(BUFFER_SIZE)
    data = data.decode("utf-8")
    print(f"[TG] Received: {data}")

print("[TG] Game started! Simulating laser tag...\n")


def recv_one():
    data, _ = recv_sock.recvfrom(BUFFER_SIZE)
    return data.decode("utf-8")


def send_event(message, friendly_fire=False, base_hit=False):
    print(f"[TG] >> {message}")
    send_sock.sendto(message.encode(), CLIENT_ADDR)
    if base_hit:
        # Model does not broadcast back for base hits — no recv needed
        return ""
    resp = recv_one()
    print(f"[TG] << {resp}")
    if friendly_fire:
        resp2 = recv_one()
        print(f"[TG] << {resp2}")
        return resp2
    return resp


game_over = False
while not game_over:
    roll = random.random()

    if roll < 0.62:
        # Cross-team takedown
        is_red_shooter = random.random() < 0.5
        shooter = random.choice(red_players if is_red_shooter else green_players)
        target = random.choice(green_players if is_red_shooter else red_players)
        resp = send_event(f"{shooter}:{target}")
        if resp == CODE_GAME_END:
            break

    elif roll < 0.77:
        # Base hit — model does not broadcast back, skip recv
        is_red_shooter = random.random() < 0.5
        shooter = random.choice(red_players if is_red_shooter else green_players)
        base = BASE_GREEN if is_red_shooter else BASE_RED
        send_event(f"{shooter}:{base}", base_hit=True)

    else:
        # Friendly fire — model broadcasts back twice (receiver penalty + hitter penalty)
        team = red_players if random.random() < 0.5 else green_players
        if len(team) < 2:
            shooter = random.choice(red_players)
            target = random.choice(green_players)
            resp = send_event(f"{shooter}:{target}")
            if resp == CODE_GAME_END:
                break
        else:
            shooter, target = random.sample(team, 2)
            resp = send_event(f"{shooter}:{target}", friendly_fire=True)
            if resp == CODE_GAME_END:
                break

    time.sleep(random.uniform(0.4, 1.8))

print("[TG] Game over. Traffic generator complete.")
