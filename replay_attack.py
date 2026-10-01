import socket
import time

LISTEN_IP = "127.0.0.1"
LISTEN_PORT = 14701

BOB_IP = "127.0.0.1"
BOB_PORT = 14601

BUFFER_SIZE = 65535

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.bind((LISTEN_IP, LISTEN_PORT))

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=" * 70)
print("REPLAY ATTACK SIMULATION")
print("=" * 70)
print(f"Listening on        : {LISTEN_IP}:{LISTEN_PORT}")
print(f"Forwarding to Bob   : {BOB_IP}:{BOB_PORT}")
print("Attack              : Capture first encrypted packet and replay it")
print("=" * 70)

captured_packet = None
packet_counter = 0

while True:
    packet, addr = receive_socket.recvfrom(BUFFER_SIZE)
    packet_counter += 1

    if captured_packet is None:
        captured_packet = packet
        print(f"\n[CAPTURE #{packet_counter}]")
        print(f"Captured encrypted packet: {len(packet)} bytes")

    send_socket.sendto(packet, (BOB_IP, BOB_PORT))

    if packet_counter <= 20:
        print(f"[FORWARD #{packet_counter}] Normal packet forwarded")

    if packet_counter == 20:
        print("\n" + "=" * 50)
        print("REPLAYING CAPTURED PACKET")
        print("=" * 50)

        time.sleep(1)

        send_socket.sendto(captured_packet, (BOB_IP, BOB_PORT))

        print("[REPLAY] Old encrypted packet sent again")
        print("Replay transmission complete — stopping attack.")
        break

receive_socket.close()
send_socket.close()
