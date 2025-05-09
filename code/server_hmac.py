import hashlib
import hmac

SECRET_KEY = b'supersecretkey'  # Unknown to attacker

def generate_mac(message: bytes) -> str:
    return hmac.new(SECRET_KEY, message, hashlib.md5).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    expected_mac = generate_mac(message)
    return hmac.compare_digest(mac, expected_mac)

def main():
    # Example message
    message = b"amount=100&to=alice"
    mac = generate_mac(message)
    print("=== Server Simulation (HMAC) ===")
    print(f"Original message: {message.decode()}")
    print(f"MAC: {mac}")
    print("\n--- Verifying legitimate message ---")
    if verify(message, mac):
        print("MAC verified successfully. Message is authentic.\n")

    forged_message = b"amount=100&to=alice" + b"&admin=true"
    #we will paste here the forged message from client.py
    #forged_message =b'amount=100&to=alice\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x01\x00\x00\x00\x00\x00\x00&admin=true'

    forged_mac = mac
    #we will paste here the forged mac from client.py
    #forged_mac = "97312a73075b6e1589117ce55e0a3ca6"
    print("--- Verifying forged message ---")
    if verify(forged_message, forged_mac):
        print("MAC verified successfully (unexpected).")
    else:
        print("MAC verification failed (as expected).")

if __name__ == "__main__":
    main()
import hashlib
import hmac
import time
import os
from typing import Tuple

# Rotate keys by storing multiple versions; index 0 is current
SECRET_KEYS = [
    b'oldsecretkey1',
    b'supersecretkey',      # key version 1
    # b'newsecretkey2',     # when you rotate, insert new key here
]
CURRENT_KEY_INDEX = 1

# How long (in seconds) we'll accept a timestamp for freshness
MAX_MESSAGE_AGE = 30

def _get_current_key() -> bytes:
    return SECRET_KEYS[CURRENT_KEY_INDEX]

def generate_mac(message: bytes, key: bytes = None) -> str:
    """
    Compute HMAC using SHA-256 and the provided key (defaults to current).
    SHA-256 avoids MD5’s collision weaknesses and is standard for HMAC.
    """
    if key is None:
        key = _get_current_key()
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def verify_mac(message: bytes, mac: str) -> bool:
    """
    Compare against all valid keys (to allow for rotation), constant-time.
    """
    for key in SECRET_KEYS:
        expected = hmac.new(key, message, hashlib.sha256).hexdigest()
        if hmac.compare_digest(mac, expected):
            return True
    return False

def pack_payload(amount: int, recipient: str) -> Tuple[bytes,str]:
    """
    Include a timestamp and random nonce to prevent replay.
    Returns (payload_bytes, mac).
    """
    timestamp = int(time.time())
    nonce = os.urandom(8).hex()       # 64-bit random nonce
    payload = f"amount={amount}&to={recipient}&t={timestamp}&n={nonce}".encode()
    mac = generate_mac(payload)
    return payload, mac

def unpack_and_verify(payload: bytes, mac: str) -> bool:
    """
    1. Verify MAC.
    2. Parse and validate timestamp freshness.
    """
    if not verify_mac(payload, mac):
        print("❌ MAC mismatch")
        return False

    # Simple parser (could use urllib.parse or JSON for real apps)
    parts = dict(item.split("=") for item in payload.decode().split("&"))
    msg_ts = int(parts.get("t", 0))
    age = time.time() - msg_ts
    if age > MAX_MESSAGE_AGE or age < -5:
        print(f"❌ Timestamp out of range (age={age:.1f}s)")
        return False

    # Additional checks could go here (e.g., amount limits)
    print("✅ Payload authenticated and fresh")
    return True

def main():
    # Server “publishes” a signed payload
    payload, mac = pack_payload(amount=100, recipient="alice")
    print("=== Server issues ===")
    print("Payload:", payload)
    print("MAC:", mac, "\n")

    # Legitimate verification
    print("=== Legitimate client ===")
    unpack_and_verify(payload, mac)
    print()

    # Simulate attacker forging by tacking on “&admin=true”
    forged = payload + b"&admin=true"
    forged_mac = mac  # attacker reuses old MAC (will fail)
    print("=== Attacker attempt ===")
    unpack_and_verify(forged, forged_mac)

if __name__ == "__main__":
    main()
