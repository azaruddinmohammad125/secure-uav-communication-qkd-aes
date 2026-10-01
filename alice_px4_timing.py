import socket
import time
import threading
import statistics
from pathlib import Path

from aes_crypto import encrypt_packet, decrypt_packet


KEY_FILE = Path(__file__).resolve().parent.parent / "session_key.bin"

WINDOWS_QGC_IP = "172.24.240.1"
QGC_PORT = 14550

ALICE_QGC_LISTEN_IP = "0.0.0.0"
ALICE_QGC_LISTEN_PORT = 14600

ALICE_SECURE_LISTEN_IP = "127.0.0.1"
ALICE_SECURE_LISTEN_PORT = 14602

BOB_SECURE_UPLINK_IP = "127.0.0.1"
BOB_SECURE_UPLINK_PORT = 14601

BUFFER_SIZE = 65535


def load_key() -> bytes:
    key = KEY_FILE.read_bytes()
    if len(key) != 32:
        raise ValueError("Session key must be exactly 32 bytes")
    return key


def qgc_to_bob(key: bytes) -> None:
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.bind((ALICE_QGC_LISTEN_IP, ALICE_QGC_LISTEN_PORT))

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sequence_number = 0
    packet_count = 0
    encryption_delays = []

    print(
        f"QGC uplink listening     : "
        f"{ALICE_QGC_LISTEN_IP}:{ALICE_QGC_LISTEN_PORT}"
    )
    print(
        f"Encrypted uplink to Bob : "
        f"{BOB_SECURE_UPLINK_IP}:{BOB_SECURE_UPLINK_PORT}"
    )

    while True:
        plaintext, source_address = receive_socket.recvfrom(BUFFER_SIZE)

        sequence_number += 1
        enc_start = time.perf_counter_ns()
        encrypted_packet = encrypt_packet(
            data=plaintext,
            key=key,
            sequence_number=sequence_number,
        )
        enc_end = time.perf_counter_ns()

        encryption_delay_ms = (enc_end - enc_start) / 1_000_000
        encryption_delays.append(encryption_delay_ms)

        send_socket.sendto(
            encrypted_packet,
            (BOB_SECURE_UPLINK_IP, BOB_SECURE_UPLINK_PORT),
        )

        packet_count += 1
        if packet_count == 1000:
            print("\n" + "=" * 65)
            print("QKD + AES-256-GCM ALICE ENCRYPTION RESULTS")
            print("=" * 65)
            print(f"Packets measured : {len(encryption_delays)}")
            print(f"Average delay    : {statistics.mean(encryption_delays):.6f} ms")
            print(f"Minimum delay    : {min(encryption_delays):.6f} ms")
            print(f"Maximum delay    : {max(encryption_delays):.6f} ms")
            print(f"Median delay     : {statistics.median(encryption_delays):.6f} ms")
            print("=" * 65)

        if packet_count <= 5 or packet_count % 100 == 0:
            print(
                f"[Alice Uplink #{packet_count}] "
                f"source={source_address} "
                f"plain={len(plaintext)}B "
                f"encrypted={len(encrypted_packet)}B "
                f"sequence={sequence_number}"
            )


def bob_to_qgc(key: bytes) -> None:
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.bind(
        (ALICE_SECURE_LISTEN_IP, ALICE_SECURE_LISTEN_PORT)
    )

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    highest_sequence = 0
    accepted_packets = 0
    rejected_packets = 0

    print(
        f"Encrypted downlink from Bob : "
        f"{ALICE_SECURE_LISTEN_IP}:{ALICE_SECURE_LISTEN_PORT}"
    )
    print(
        f"Plaintext downlink to QGC    : "
        f"{WINDOWS_QGC_IP}:{QGC_PORT}"
    )

    while True:
        encrypted_packet, source_address = receive_socket.recvfrom(
            BUFFER_SIZE
        )

        try:
            sequence_number, plaintext = decrypt_packet(
                packet=encrypted_packet,
                key=key,
            )

            if sequence_number <= highest_sequence:
                rejected_packets += 1
                print(
                    f"[Alice DOWNLINK REJECTED] Replay detected "
                    f"sequence={sequence_number}, "
                    f"highest={highest_sequence}"
                )
                continue

            highest_sequence = sequence_number

            send_socket.sendto(
                plaintext,
                (WINDOWS_QGC_IP, QGC_PORT),
            )

            accepted_packets += 1

            if accepted_packets <= 5 or accepted_packets % 100 == 0:
                print(
                    f"[Alice Downlink #{accepted_packets}] "
                    f"source={source_address} "
                    f"plain={len(plaintext)}B "
                    f"sequence={sequence_number} "
                    f"authentication=PASSED"
                )

        except ValueError as error:
            rejected_packets += 1
            print(
                f"[Alice DOWNLINK REJECTED] "
                f"Authentication failed: {error}"
            )


def main() -> None:
    key = load_key()

    print("=" * 72)
    print("ALICE PX4 BIDIRECTIONAL QKD + AES-256-GCM GATEWAY")
    print("=" * 72)
    print(f"Session key length : {len(key)} bytes")
    print("Authentication     : AES-GCM")
    print("Anti-replay        : Sequence-number validation")
    print("Status             : RUNNING")
    print("=" * 72)

    uplink_thread = threading.Thread(
        target=qgc_to_bob,
        args=(key,),
        daemon=True,
    )

    downlink_thread = threading.Thread(
        target=bob_to_qgc,
        args=(key,),
        daemon=True,
    )

    uplink_thread.start()
    downlink_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAlice PX4 gateway stopped")


if __name__ == "__main__":
    main()
