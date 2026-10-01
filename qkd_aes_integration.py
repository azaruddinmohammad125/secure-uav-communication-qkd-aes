from bb84 import generate_bb84_key
from aes_crypto import decrypt_packet, encrypt_packet


def main() -> None:
    aes_key, bb84_stats = generate_bb84_key(num_bits=512)

    test_payload = b"PX4 MAVLink secure telemetry packet"
    sequence_number = 1

    encrypted_packet = encrypt_packet(
        data=test_payload,
        key=aes_key,
        sequence_number=sequence_number,
    )

    received_sequence, decrypted_payload = decrypt_packet(
        packet=encrypted_packet,
        key=aes_key,
    )

    print("=" * 65)
    print("QKD + AES-256-GCM Integration Test")
    print("=" * 65)
    print(f"BB84 original bits     : {bb84_stats['original_bits']}")
    print(f"BB84 sifted bits       : {bb84_stats['sifted_bits']}")
    print(f"BB84 QBER              : {bb84_stats['qber'] * 100:.2f}%")
    print(f"Derived AES key length : {len(aes_key)} bytes")
    print(f"Original payload       : {test_payload}")
    print(f"Encrypted packet size  : {len(encrypted_packet)} bytes")
    print(f"Received sequence      : {received_sequence}")
    print(f"Decrypted payload      : {decrypted_payload}")
    print(
        "Payload match          :",
        "PASSED" if decrypted_payload == test_payload else "FAILED",
    )
    print("=" * 65)


if __name__ == "__main__":
    main()
