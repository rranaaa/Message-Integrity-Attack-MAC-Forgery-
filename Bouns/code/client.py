import hashpumpy
import hashlib
from urllib.parse import quote
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Server's verify function (copied for testing)
SECRET_KEY = b'supersecretkey'  # For testing; attacker doesn't know this
def generate_mac(message: bytes) -> str:
    return hashlib.md5(SECRET_KEY + message).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    expected_mac = generate_mac(message)
    return mac == expected_mac

def perform_attack():
    # Intercepted message and MAC (from server.py output)
    intercepted_message = b"amount=100&to=alice"
    intercepted_mac = input("Enter the intercepted MAC from server.py: ").strip()
    data_to_append = b"&admin=true"

    # Guess secret key length (14 bytes for 'supersecretkey')
    key_length = 14  # In practice, attacker tries multiple lengths

    try:
        # Perform length extension attack
        new_mac, new_message = hashpumpy.hashpump(
            intercepted_mac,       # Original MAC (hex string)
            intercepted_message,   # Original message (bytes)
            data_to_append,        # Data to append (bytes)
            key_length             # Secret key length
        )
    except Exception as e:
        print(f"Error with hashpumpy: {e}")
        print("Ensure hashpumpy is installed and compatible with your Python version.")
        return

    forged_message = new_message
    forged_mac = new_mac

    print("=== Length Extension Attack ===")
    print(f"Intercepted message: {intercepted_message.decode()}")
    print(f"Intercepted MAC: {intercepted_mac}")
    print(f"Data to append: {data_to_append.decode()}")
    print(f"Forged message: {quote(forged_message.decode('latin1'))}")
    print(f"Forged MAC: {forged_mac}")

    # Verify the forged message
    print("\n--- Verifying forged message ---")
    if verify(forged_message, forged_mac):
        print("MAC verified successfully (attack succeeded).")
    else:
        print("MAC verification failed (attack failed).")

    # Save forged message and MAC for server.py
    print("\nCopy these for server.py:")
    print(f"forged_message = {forged_message!r}")
    print(f"forged_mac = \"{forged_mac}\"")
if __name__ == "__main__":
    perform_attack()
