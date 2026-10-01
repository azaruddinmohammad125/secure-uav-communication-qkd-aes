import socket
import time
from pathlib import Path

from aes_crypto import encrypt_packet


KEY_FILE = Path(__file__).resolve().parent.parent / "session_key.bin"

ALICE_LISTEN_IP = "0.0.0.0"
ALICE_LISTEN_PORT = 14600

BOB_IP = "127.0.0.1"
BOB_SECURE_PORT = 14601

BUFFER_SIZE = 65535


def load_key() -> bytes:
    key = KEY_FILE.read_bytes()

    if len(key) != 32:
        raise ValueError("Session key must be exactly 32 bytes")

    return key


def main() -> None:
    key = load_key()

    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.bind((ALICE_LISTEN_IP, ALICE_LISTEN_PORT))

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sequence_number = 0
    packet_count = 0
    total_plaintext_bytes = 0
    total_encrypted_bytes = 0
    start_time = time.time()

    print("=" * 65)
    print("ALICE QKD + AES-256-GCM ENCRYPTION PROXY")
    print("=" * 65)
    print(f"Listening for plaintext : {ALICE_LISTEN_IP}:{ALICE_LISTEN_PORT}")
    print(f"Sending encrypted data  : {BOB_IP}:{BOB_SECURE_PORT}")
    print(f"Session key length      : {len(key)} bytes")
    print("Status                  : RUNNING")
    print("=" * 65)

    try:
        while True:
            plaintext, source_address = receive_socket.recvfrom(BUFFER_SIZE)

            sequence_number += 1

            encrypted_packet = encrypt_packet(
                data=plaintext,
                key=key,
                sequence_number=sequence_number,
            )

            send_socket.sendto(
                encrypted_packet,
                (BOB_IP, BOB_SECURE_PORT),
            )

            packet_count += 1
            total_plaintext_bytes += len(plaintext)
            total_encrypted_bytes += len(encrypted_packet)

            if packet_count <= 5 or packet_count % 100 == 0:
                print(
                    f"[Alice #{packet_count}] "
                    f"source={source_address} "
                    f"plain={len(plaintext)}B "
                    f"encrypted={len(encrypted_packet)}B "
                    f"sequence={sequence_number}"
                )

    except KeyboardInterrupt:
        elapsed = time.time() - start_time

        print("\n" + "=" * 65)
        print("Alice proxy stopped")
        print(f"Packets encrypted       : {packet_count}")
        print(f"Plaintext bytes         : {total_plaintext_bytes}")
        print(f"Encrypted bytes         : {total_encrypted_bytes}")
        print(f"Runtime                  : {elapsed:.2f} seconds")
        print("=" * 65)

    finally:
        receive_socket.close()
        send_socket.close()


if __name__ == "__main__":
    main()
