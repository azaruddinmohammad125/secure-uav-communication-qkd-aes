import socket
import time

DESTINATION = ("127.0.0.1", 14700)

messages = [
    b"UAV telemetry packet 1: GPS=52.9548,-1.1581",
    b"UAV telemetry packet 2: GPS=52.9549,-1.1582",
    b"UAV telemetry packet 3: GPS=52.9550,-1.1583",
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for index, message in enumerate(messages, start=1):
    sock.sendto(message, DESTINATION)
    print(f"Sent plaintext packet {index}: {message}")
    time.sleep(1)

sock.close()
