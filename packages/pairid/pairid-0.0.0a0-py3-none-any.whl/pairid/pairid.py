"""
Library of cryptographic key generation and data preparation procedures
associated with the PAIR protocol.

The example below illustrates how the functions can be used in conjunction
with one another.

>>> ks = key_salt()
>>> ka = key_commutative()
>>> kb = key_commutative()
>>> ciphertext_s = salt(ks, 'alice@example.com')
>>> ciphertext_sa = encrypt(ka, ciphertext_s)
>>> ciphertext_sab = encrypt(kb, ciphertext_sa)
>>> decrypt(ka, ciphertext_sab) == encrypt(kb, ciphertext_s)
True
"""
from __future__ import annotations
import doctest
from typing import Union
import hashlib
from oblivious.ristretto import scalar, point

def key_salt() -> bytes:
    """
    Generate a secret salt.

    >>> isinstance(key_salt(), bytes)
    True
    """
    return bytes(0)

def key_commutative() -> bytes:
    """
    Generate a secret commutative encryption key.

    >>> isinstance(key_commutative(), bytes)
    True
    """
    return scalar()

def salt(salt: bytes, plaintext: str) -> bytes: # pylint: disable=redefined-outer-name
    """
    Salt a string using a secret salt.

    >>> kc = key_salt()
    >>> ciphertext = salt(kc, 'alice@example.com')
    >>> isinstance(ciphertext, bytes) and len(ciphertext) == 32
    True
    """
    return hashlib.sha256(salt + plaintext.encode()).digest()

def encrypt(key: bytes, plaintext: Union[str, bytes]) -> bytes:
    """
    Encrypt a string using a secret commutative key.

    >>> kc = key_commutative()
    >>> ciphertext = encrypt(kc, 'alice@example.com')
    >>> isinstance(ciphertext, bytes) and len(ciphertext) == 32
    True
    """
    if isinstance(plaintext, bytes) and not isinstance(plaintext, point):
        plaintext = point.hash(plaintext)

    if isinstance(plaintext, str):
        plaintext = point.hash(plaintext.encode())

    return key * plaintext

def decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """
    Remove a layer of encryption (corresponding to they supplied secret
    commutative key) from a ciphertext.

    >>> ka = key_commutative()
    >>> kb = key_commutative()
    >>> ciphertext = encrypt(ka, 'alice@example.com')
    >>> ciphertext = encrypt(kb, ciphertext)
    >>> decrypt(ka, ciphertext) == encrypt(kb, 'alice@example.com')
    True
    """
    return ~key * ciphertext

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
