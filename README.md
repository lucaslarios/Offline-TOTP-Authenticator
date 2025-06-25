# Offline TOTP Authenticator

This project is a secure, offline TOTP (Time-based One-Time Password) Authenticator built with Python, using:

- 🐍 Python + Tkinter for GUI
- 🔐 AES-256 (CBC mode) for encryption
- 🧂 PBKDF2 and Scrypt for key derivation and password hashing
- 🗄️ SQLite for local data storage
- 🔑 pyotp for TOTP generation (RFC 6238)

---

## 📦 Features

- Offline, secure, portable TOTP manager
- Each user account is protected by a password
- Each TOTP URI is encrypted using a symmetric key derived from the user's password
- TOTP secrets are never stored in plaintext
- Compatible with Google Authenticator-style URIs
- Passwords are stored using Scrypt for resistance against brute-force attacks

---

## 🔐 Security Architecture

| Component         | Technique                             |
|-------------------|----------------------------------------|
| TOTP URI storage  | AES-256 in CBC mode                    |
| IV                | Random 16-byte IV per encryption       |
| Key derivation    | PBKDF2 with 1,000,000 iterations       |
| Data encoding     | Base64 for storage in SQLite           |


---

## 🧠 How It Works

1. User registers with a username and password.
2. Two salts are generated:
   - One for password hashing (Scrypt)
   - One for TOTP encryption key derivation (PBKDF2)
3. TOTP URIs are encrypted using AES-CBC with the key derived from the user's password.
4. When logging in, the same password regenerates the key, which is used to decrypt all stored TOTP URIs.
5. The application displays the current TOTP codes in real time.

---

## 🚀 How to Run


1. **Configure venv**
    ```bash
   python3 -m venv .venv
   ```
   ```bash
   source .venv/bin/activate 
   ```
2. **Install dependencies**

   Make sure you have Python installed (version 3.7 or higher). Then, install the required packages with:

   ```bash
   pip install -r requirements.txt
    ```

3. **Run the application**

   To launch the authenticator, run the following command from the root directory:

   ```bash
   python3 controller/controller.py
   ```

