import socket
import time

DESTINATION_IP = "127.0.0.1"
DESTINATION_PORT = 14600

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=" * 55)
print("TEST SENDER")
print("=" * 55)

messages = [
    b"Telemetry Packet 1",
    b"Telemetry Packet 2",
    b"Telemetry Packet 3",
    b"Telemetry Packet 4",
    b"Telemetry Packet 5",
]

for i, message in enumerate(messages, start=1):
    sock.sendto(message, (DESTINATION_IP, DESTINATION_PORT))
    print(f"Sent Packet {i}: {message}")
    time.sleep(1)

print("\nAll packets sent successfully.")
