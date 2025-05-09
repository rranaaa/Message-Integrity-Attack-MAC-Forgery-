# Message-Integrity-Attack-MAC-Forgery-
Sure! Below is a sample **README** file for the project hosted on the GitHub link you provided. It explains the **Message Integrity Attack and MAC Forgery** concept and provides details about how to use and contribute to the repository.

---

# Message Integrity Attack (MAC Forgery)

This repository demonstrates a **Message Integrity Attack** and how **MAC Forgery** can be exploited through **length extension attacks** on hash-based message authentication codes (MACs). The project showcases how an attacker can forge a valid MAC for a modified message without knowing the secret key.

##  Overview

In the context of **Message Authentication Codes (MACs)**, an attacker can exploit certain weaknesses in hash functions like MD5 to forge a valid MAC for a modified message. This is known as a **length extension attack**. The attacker doesn't need to know the secret key but can **append** new data to a message and compute a new valid MAC.

This project demonstrates:

* **MD5 Padding** and its vulnerabilities in the context of MAC.
* **Length Extension Attacks** on an MD5-based MAC.
* How **HMAC** (Hash-based Message Authentication Code) can defend against these attacks.

##  Features

* **Length Extension Attack Simulation**:

  * Intercept the original message and MAC.
  * Use a library like `hashpumpy` to perform the attack and forge a new valid MAC for a modified message.
* **HMAC Defense**:

  * Implement HMAC to demonstrate how it mitigates the length extension attack.
* **Real-world Example**:

  * Example with both **original message** and **forged message** using MD5.

## Installation

1. **Clone this repository** to your local machine:

   ```bash
   git clone https://github.com/rranaaa/Message-Integrity-Attack-MAC-Forgery.git
   cd Message-Integrity-Attack-MAC-Forgery
   ```

2. **Install dependencies**:
   This project requires `hashpumpy` and `hmac` to perform the attack and simulate the defense.

   ```bash
   pip install hashpumpy
   ```

3. **Run the attack**:
   After cloning the repository and installing the dependencies, you can run the attack script:

   ```bash
   python attack_simulation.py
   ```

4. **(Optional) Try with HMAC**:
   To see how **HMAC** can protect against such attacks, you can modify the script to use HMAC instead of the vulnerable MD5-based MAC. Check the `hmac_defense.py` file.

## Usage

1. **Original MAC Verification**:

   * The attacker intercepts the **original message** and its **MAC**.
2. **Length Extension Attack**:

   * The attacker appends additional data (e.g., `&admin=true`) to the message.
   * The attacker uses `hashpumpy` to compute a new valid MAC for the **modified message**.
3. **Verification of Forged MAC**:

   * The forged message and MAC are sent to the server.
   * The server verifies the MAC and accepts the forged message if the attack is successful.
4. **HMAC Protection**:

   * Use HMAC to prevent the length extension attack.
   * Modify the script to compute HMAC for both the message and the forged message.

## Example

### **Length Extension Attack Simulation**:

```python
import hashpumpy

# Intercepted message and MAC
intercepted_message = b"amount=100&to=alice"
intercepted_mac = input("Enter intercepted MAC: ").strip()
data_to_append = b"&admin=true"
key_length = 14  # Length of the secret key

# Perform attack
new_mac, new_message = hashpumpy.hashpump(intercepted_mac, intercepted_message, data_to_append, key_length)

# Output forged message and MAC
print(f"Forged message: {new_message.decode()}")
print(f"Forged MAC: {new_mac}")
```

### **HMAC Defense Example**:

```python
import hmac
import hashlib

# Secret key (known only to server)
secret_key = b'supersecretkey'

# Message to authenticate
message = b"amount=100&to=alice"

# Create HMAC using SHA-256
mac = hmac.new(secret_key, message, hashlib.sha256)

# Print the HMAC value (the MAC)
print("Generated HMAC:", mac.hexdigest())

# To verify the HMAC:
def verify_mac(message, mac, key):
    calculated_mac = hmac.new(key, message, hashlib.sha256).hexdigest()
    return mac == calculated_mac

# Example of verification
if verify_mac(message, mac.hexdigest(), secret_key):
    print("HMAC verification succeeded.")
else:
    print("HMAC verification failed.")
```

---

## Security Warning

* **MD5 and other weak hash functions** are **not recommended** for securing sensitive data. They are vulnerable to length extension attacks.
* Always use **stronger hash functions** (e.g., SHA-256) combined with HMAC for integrity and authenticity.
* **HMAC** is a more secure alternative to simple MACs and ensures that **no valid MAC** can be forged without the secret key.



## Contributing

Contributions are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.

1. **Fork the repository**.
2. **Clone your fork** to your local machine:

   ```bash
   git clone https://github.com/your-username/Message-Integrity-Attack-MAC-Forgery.git
   ```
3. **Create a new branch** for your changes:

   ```bash
   git checkout -b new-feature
   ```
4. **Make your changes**, then **commit** them:

   ```bash
   git commit -m "Added new feature"
   ```
5. **Push** to your fork:

   ```bash
   git push origin new-feature
   ```
6. **Submit a pull request** to the main repository.


