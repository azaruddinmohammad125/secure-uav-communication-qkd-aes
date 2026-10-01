import socket
import time
import statistics

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 14600

FORWARD_IP = "172.24.240.1"
FORWARD_PORT = 18570

TARGET_PACKETS = 1000
BUFFER_SIZE = 65535

recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind((LISTEN_IP, LISTEN_PORT))

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

delays = []

print("=" * 65)
print("UNSECURED MAVLink PACKET PROCESSING DELAY TEST")
print("=" * 65)
print(f"Listening   : {LISTEN_IP}:{LISTEN_PORT}")
print(f"Forwarding  : {FORWARD_IP}:{FORWARD_PORT}")
print(f"Packets     : {TARGET_PACKETS}")
print("=" * 65)

for packet_no in range(1, TARGET_PACKETS + 1):

    packet, source = recv_socket.recvfrom(BUFFER_SIZE)

    start = time.perf_counter_ns()

    send_socket.sendto(
        packet,
        (FORWARD_IP, FORWARD_PORT)
    )

    end = time.perf_counter_ns()

    delay_ms = (end - start) / 1_000_000
    delays.append(delay_ms)

    if packet_no <= 5 or packet_no % 100 == 0:
        print(
            f"[Packet #{packet_no}] "
            f"size={len(packet)}B "
            f"delay={delay_ms:.6f} ms"
        )

print("\n" + "=" * 65)
print("UNSECURED BASELINE RESULTS")
print("=" * 65)
print(f"Packets measured : {len(delays)}")
print(f"Average delay    : {statistics.mean(delays):.6f} ms")
print(f"Minimum delay    : {min(delays):.6f} ms")
print(f"Maximum delay    : {max(delays):.6f} ms")
print(f"Median delay     : {statistics.median(delays):.6f} ms")
print("=" * 65)

recv_socket.close()
send_socket.close()
