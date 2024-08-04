"""
module docstring should be here

See the companion `.md` file.
"""

import hashlib
import os

from typing import Final

# Example pepper value
PEPPER: Final[str] = os.environ.get('PEPPER', 'n1G3p!K8O6E9A5)d4I0h2M4.j1lC7f3b2')


def hash_password(password: str, salt: str) -> str:
    # Combine password, salt, and pepper
    combined = password + salt + PEPPER
    # Hash the combined string
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()


def main():
    password: Final[str] = "user_password"
    salt: Final[str] = os.urandom(16).hex()
    hashed_password: Final[str] = hash_password(password, salt)
    print(f"Salt: {salt} (length: {len(salt)})")
    print(f"Hashed Password: {hashed_password} (length: {len(hashed_password)})")


if __name__ == '__main__':
    main()
