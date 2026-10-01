from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt_packet(data: bytes, key: bytes, sequence_number: int) -> bytes:
    """
    Encrypts a MAVLink packet using AES-256-GCM.

    Packet format:
    [8-byte sequence number][12-byte nonce][16-byte tag][ciphertext]
    """
    if len(key) != 32:
        raise ValueError("AES-256 requires a 32-byte key")

    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    sequence_bytes = sequence_number.to_bytes(8, byteorder="big")
    cipher.update(sequence_bytes)

    ciphertext, tag = cipher.encrypt_and_digest(data)

    return sequence_bytes + nonce + tag + ciphertext


def decrypt_packet(packet: bytes, key: bytes) -> tuple[int, bytes]:
    """
    Decrypts and authenticates an AES-256-GCM packet.
    Returns:
        sequence_number, plaintext
    """
    if len(packet) < 36:
        raise ValueError("Encrypted packet is too short")

    sequence_bytes = packet[:8]
    nonce = packet[8:20]
    tag = packet[20:36]
    ciphertext = packet[36:]

    sequence_number = int.from_bytes(sequence_bytes, byteorder="big")

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(sequence_bytes)

    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    return sequence_number, plaintext


if __name__ == "__main__":
    test_key = get_random_bytes(32)
    test_message = b"PX4 MAVLink test packet"
    test_sequence = 1

    encrypted = encrypt_packet(test_message, test_key, test_sequence)
    sequence, decrypted = decrypt_packet(encrypted, test_key)

    print("=" * 55)
    print("AES-256-GCM Module Test")
    print("=" * 55)
    print(f"Original message : {test_message}")
    print(f"Encrypted length : {len(encrypted)} bytes")
    print(f"Sequence number  : {sequence}")
    print(f"Decrypted message: {decrypted}")
    print("Authentication   : PASSED")
    print("=" * 55)
