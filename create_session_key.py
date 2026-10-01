from pathlib import Path

from bb84 import generate_bb84_key


KEY_FILE = Path(__file__).resolve().parent.parent / "session_key.bin"


def main() -> None:
    key, stats = generate_bb84_key(num_bits=512)

    if stats["qber"] > 0.11:
        raise RuntimeError(
            f"QBER {stats['qber'] * 100:.2f}% exceeds 11% threshold"
        )

    KEY_FILE.write_bytes(key)
    KEY_FILE.chmod(0o600)

    print("=" * 60)
    print("QKD Session Key Generation")
    print("=" * 60)
    print(f"Original bits   : {stats['original_bits']}")
    print(f"Sifted bits     : {stats['sifted_bits']}")
    print(f"QBER            : {stats['qber'] * 100:.2f}%")
    print(f"AES key length  : {len(key)} bytes")
    print(f"Key file        : {KEY_FILE}")
    print("Key status      : CREATED")
    print("=" * 60)


if __name__ == "__main__":
    main()
