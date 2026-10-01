import socket

MITM_IP = "127.0.0.1"
MITM_PORT = 14701

BOB_IP = "127.0.0.1"
BOB_PORT = 14601

BUFFER_SIZE = 65535

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.bind((MITM_IP, MITM_PORT))

forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=" * 70)
print("MITM ATTACK SIMULATION — WITH QKD + AES-256-GCM")
print("=" * 70)
print(f"Intercepting encrypted : {MITM_IP}:{MITM_PORT}")
print(f"Forwarding to Bob      : {BOB_IP}:{BOB_PORT}")
print("Attack action          : Modify encrypted ciphertext")
print("Expected defence       : AES-GCM authentication failure")
print("Status                 : RUNNING")
print("=" * 70)

packet_count = 0

try:
    while True:
        encrypted_packet, source_address = receive_socket.recvfrom(BUFFER_SIZE)
        packet_count += 1

        tampered_packet = bytearray(encrypted_packet)

        # Change one ciphertext byte without knowing the AES key.
        if len(tampered_packet) > 36:
            tampered_packet[-1] ^= 0x01
        else:
            tampered_packet[-1] ^= 0x01

        forward_socket.sendto(
            bytes(tampered_packet),
            (BOB_IP, BOB_PORT),
        )

        print(f"\n[SECURE MITM #{packet_count}]")
        print(f"Source               : {source_address}")
        print(f"Encrypted packet size: {len(encrypted_packet)} bytes")
        print("Ciphertext modified  : YES")
        print("Forwarded to Bob     : YES")

except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print("Secure MITM simulation stopped")
    print(f"Packets tampered: {packet_count}")
    print("=" * 70)

finally:
    receive_socket.close()
    forward_socket.close()
