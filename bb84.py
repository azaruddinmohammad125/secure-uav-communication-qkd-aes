import hashlib
import random


def generate_bb84_key(num_bits: int = 512) -> tuple[bytes, dict]:
    """Simulate BB84 and derive a 32-byte AES-256 key."""

    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_bases = [random.choice(["+", "x"]) for _ in range(num_bits)]
    bob_bases = [random.choice(["+", "x"]) for _ in range(num_bits)]

    bob_bits = []

    for index in range(num_bits):
        if alice_bases[index] == bob_bases[index]:
            bob_bits.append(alice_bits[index])
        else:
            bob_bits.append(random.randint(0, 1))

    alice_sifted = []
    bob_sifted = []

    for index in range(num_bits):
        if alice_bases[index] == bob_bases[index]:
            alice_sifted.append(alice_bits[index])
            bob_sifted.append(bob_bits[index])

    if not alice_sifted:
        raise RuntimeError("BB84 sifting produced an empty key")

    error_count = sum(
        alice_bit != bob_bit
        for alice_bit, bob_bit in zip(alice_sifted, bob_sifted)
    )

    qber = error_count / len(alice_sifted)

    shared_bit_string = "".join(str(bit) for bit in alice_sifted)
    aes_key = hashlib.sha256(shared_bit_string.encode("utf-8")).digest()

    stats = {
        "original_bits": num_bits,
        "sifted_bits": len(alice_sifted),
        "errors": error_count,
        "qber": qber,
        "aes_key_hex": aes_key.hex(),
    }

    return aes_key, stats


if __name__ == "__main__":
    key, statistics = generate_bb84_key()

    print("=" * 60)
    print("BB84 QKD Simulation")
    print("=" * 60)
    print(f"Original bits      : {statistics['original_bits']}")
    print(f"Sifted bits        : {statistics['sifted_bits']}")
    print(f"Errors             : {statistics['errors']}")
    print(f"QBER               : {statistics['qber'] * 100:.2f}%")
    print(f"AES-256 key length : {len(key)} bytes")
    print(f"AES-256 key (HEX)  : {statistics['aes_key_hex']}")
    print("=" * 60)
