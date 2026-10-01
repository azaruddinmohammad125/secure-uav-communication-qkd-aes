import socket

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 14602

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print("=" * 55)
print("TEST RECEIVER")
print("=" * 55)
print(f"Listening on {LISTEN_IP}:{LISTEN_PORT}")
print("=" * 55)

while True:
    data, addr = sock.recvfrom(65535)

    print()
    print("Packet received!")
    print(f"From    : {addr}")
    print(f"Length  : {len(data)} bytes")
    print(f"Payload : {data}")
