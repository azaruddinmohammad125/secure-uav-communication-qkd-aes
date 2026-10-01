import socket
import time
from pathlib import Path

from aes_crypto import decrypt_packet


KEY_FILE = Path(__file__).resolve().parent.parent / "session_key.bin"

BOB_LISTEN_IP = "127.0.0.1"
BOB_SECURE_PORT = 14601

FORWARD_IP = "172.24.240.1"
FORWARD_PORT = 18570

BUFFER_SIZE = 65535


def load_key() -> bytes:
    key = KEY_FILE.read_bytes()

    if len(key) != 32:
        raise ValueError("Session key must be exactly 32 bytes")

    return key


def main() -> None:
    key = load_key()

    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.bind((BOB_LISTEN_IP, BOB_SECURE_PORT))

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    highest_sequence = 0
    accepted_packets = 0
    rejected_packets = 0
    total_plaintext_bytes = 0
    start_time = time.time()

    print("=" * 65)
    print("BOB QKD + AES-256-GCM DECRYPTION PROXY")
    print("=" * 65)
    print(f"Listening for encrypted : {BOB_LISTEN_IP}:{BOB_SECURE_PORT}")
    print(f"Forwarding plaintext    : {FORWARD_IP}:{FORWARD_PORT}")
    print(f"Session key length      : {len(key)} bytes")
    print("Authentication          : AES-GCM")
    print("Anti-replay             : Sequence-number validation")
    print("Status                  : RUNNING")
    print("=" * 65)

    try:
        while True:
            encrypted_packet, source_address = receive_socket.recvfrom(BUFFER_SIZE)

            try:
                sequence_number, plaintext = decrypt_packet(
                    packet=encrypted_packet,
                    key=key,
                )

                if sequence_number <= highest_sequence:
                    rejected_packets += 1
                    print(
                        f"[REJECTED] Replay detected "
                        f"sequence={sequence_number}, "
                        f"highest={highest_sequence}"
                    )
                    continue

                highest_sequence = sequence_number

                send_socket.sendto(
                    plaintext,
                    (FORWARD_IP, FORWARD_PORT),
                )

                accepted_packets += 1
                total_plaintext_bytes += len(plaintext)

                if accepted_packets <= 5 or accepted_packets % 100 == 0:
                    print(
                        f"[Bob #{accepted_packets}] "
                        f"source={source_address} "
                        f"plain={len(plaintext)}B "
                        f"sequence={sequence_number} "
                        f"authentication=PASSED"
                    )

            except ValueError as error:
                rejected_packets += 1
                print(
                    f"[REJECTED] Authentication failed: {error}"
                )

    except KeyboardInterrupt:
        elapsed = time.time() - start_time

        print("\n" + "=" * 65)
        print("Bob proxy stopped")
        print(f"Accepted packets        : {accepted_packets}")
        print(f"Rejected packets        : {rejected_packets}")
        print(f"Plaintext bytes          : {total_plaintext_bytes}")
        print(f"Highest sequence         : {highest_sequence}")
        print(f"Runtime                  : {elapsed:.2f} seconds")
        print("=" * 65)

    finally:
        receive_socket.close()
        send_socket.close()


if __name__ == "__main__":
    main()
