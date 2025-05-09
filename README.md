# Message Integrity Attack — MAC Forgery via Length Extension

This project demonstrates a practical implementation of a **length extension attack** on MACs (Message Authentication Codes) constructed using insecure hash functions like MD5.

## Project Structure

```
Message-Integrity-Attack-MAC-Forgery-/
├── code/
│   ├── server.py         # Simulates server-side MAC generation and verification
│   ├── client.py         # Performs the length extension attack using hashpumpy
│   └── explanation.py    # Walkthrough and explanation of padding and internals
├── Demo assignment.pdf   # Written report explaining the concepts
└── README.md             # Project overview and usage instructions
```

---

## Objective

To demonstrate how using a construction like `MAC = MD5(secret_key || message)` is **insecure**, as it allows attackers to:

* Guess the secret key length
* Extend a valid MAC to include attacker-controlled data
* Bypass integrity checks

---

##  Requirements

* Python 3.6+
* `hashpumpy` module

Install dependencies:

```bash
pip install hashpumpy
```

---

## How to Run

### Step 1: Simulate the Server

```bash
cd code
python server.py
```

This will print the legitimate message and its MAC.

### Step 2: Perform the Attack

Run the attack from the client side:

```bash
python client.py
```

It will ask you to paste the MAC printed by the server. It will then forge a new message and MAC.

### Step 3: Copy to Server for Verification

In `client.py`, you will see output like:

```text
Copy these for server.py:
forged_message = b'...'
forged_mac = "..."
```

Paste those into `server.py` (in the indicated section), then re-run it. If successful, it will say:

```
MAC verified successfully (unexpected).
```

---

## Understanding the Attack

Run the walkthrough file for step-by-step insights into the Merkle–Damgård construction and padding:

```bash
python explanation.py
```

This explains how MD5 pads messages and why it's vulnerable to length extension attacks.

---

## Defense Strategy

Use **HMAC** instead of naïve constructions:

```python
import hmac
mac = hmac.new(secret_key, message, hashlib.md5).hexdigest()
```

HMAC prevents internal state recovery, making length extension attacks ineffective.

---

##
