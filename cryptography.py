"""
module docstring should be here

See the companion `.md` file.
"""

import hashlib
import os
import scrypt

from typing import Final

# Example pepper value
PEPPER: Final[str] = os.environ.get('PEPPER', 'n1G3p!K8O6E9A5)d4I0h2M4.j1lC7f3b2')


def hash_a_combined_password_with_salt_and_pepper_using_sha256() -> None:
    password: Final[str] = "user_password"
    salt: Final[str] = os.urandom(16).hex()

    # Combine password, salt, and pepper
    combined_password: Final[str] = password + salt + PEPPER
    # Hash the combined string
    hashed_password: Final[str] = hashlib.sha256(combined_password.encode('utf-8')).hexdigest()

    print(f"Salt: {salt} (length: {len(salt)})")
    print(f"Hashed Password: {hashed_password} (length: {len(hashed_password)})")


def hash_a_combined_password_with_salt_and_pepper_using_scrypt() -> None:
    # Generate a random salt
    salt: Final[bytes] = os.urandom(16)

    # Define the pepper (kept secure, not stored in the database)
    pepper: Final[bytes] = b'your_secret_pepper'

    # User's password
    password: Final[bytes] = b'your_password'

    # Combine password, salt, and pepper
    combined_password: Final[bytes] = password + salt + pepper

    # Hash the combined string using scrypt
    hashed_password: Final[bytes] = scrypt.hash(combined_password, salt, N=16384, r=8, p=1)

    # Store the salt and hashed password in the database
    # Note: The pepper is not stored in the database

    print(f"Salt: {salt!r} (length: {len(salt)})")
    print(f"Hashed Password: {hashed_password!r} (length: {len(hashed_password)})")


def main():
    hash_a_combined_password_with_salt_and_pepper_using_sha256()
    hash_a_combined_password_with_salt_and_pepper_using_scrypt()


if __name__ == '__main__':
    main()
