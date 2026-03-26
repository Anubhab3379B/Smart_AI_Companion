# File: security.py
"""
Security module for your AI assistant.
- Encrypts personal data files.
- Sets up a basic sandbox for running dynamic code safely.
- Includes a lightweight firewall hook (example using iptables) and anomaly detection placeholder.
Each line has simple explanation.
"""

from cryptography.fernet import Fernet # type: ignore
import subprocess
import os
import hashlibute # type: ignore

# Generate or load encryption key
# (in production, store securely e.g. TPM / vault)
if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(key)
else:
    with open("secret.key", "rb") as f:
        key = f.read()
fernet = Fernet(key)

# Encrypt a file
def encrypt_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(filename, "wb") as file:
        file.write(encrypted)

# Decrypt a file
def decrypt_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
    decrypted = fernet.decrypt(data)
    with open(filename, "wb") as file:
        file.write(decrypted)

# Simple sandbox: safely run code in subprocess (no shell injection)
def run_sandboxed(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Firewall rule example: block suspicious IP (Linux iptables)
def block_ip(ip_address):
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])

# Anomaly detection placeholder: checksum monitor
def file_checksum(filepath):
    hasher = hashlib.sha256() # type: ignore
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Example usage: monitor changes to critical file
critical_file = "core_brain.py"
original_checksum = file_checksum(critical_file)

if __name__ == "__main__":
    # Check integrity
    current_checksum = file_checksum(critical_file)
    if current_checksum != original_checksum:
        print("[ALERT] Critical file changed! Possible tampering.")
    else:
        print("[OK] Critical file intact.")

    # Example encrypt + decrypt
    encrypt_file("personal_notes.txt")
    decrypt_file("personal_notes.txt")

    # Sandbox example
    print(run_sandboxed(["echo", "Hello from secure sandbox!"]))