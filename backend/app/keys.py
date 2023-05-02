import textwrap
from base64 import urlsafe_b64decode, urlsafe_b64encode
from functools import cached_property
from hashlib import sha256

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from pydantic import SecretStr


def urlsafe_b64_to_unsigned_int(s: str) -> int:
    """
    Decode urlsafe base64 to unsigned integers.
    """
    while len(s) % 4 != 0:
        s += "="
    return int.from_bytes(urlsafe_b64decode(s), byteorder="big", signed=False)


def unsigned_int_to_urlsafe_b64(i: int) -> str:
    """
    Encode unsigned integers as urlsafe base64 strings.
    """

    def byte_len(n):
        length = 0
        while n > 0:
            length += 1
            n = n >> 8
        return length

    byte_str = int.to_bytes(i, length=byte_len(i), byteorder="big", signed=False)
    return urlsafe_b64encode(byte_str).decode().rstrip("=")


class RsaPrivateKey(SecretStr):
    def __init__(self, value: str):
        super().__init__(textwrap.dedent(value).strip())

    def __repr__(self) -> str:
        return f"RsaPrivateKey('{self}')"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        yield cls.check_rsa

    @classmethod
    def check_rsa(cls, value):
        serialization.load_pem_private_key(
            value.get_secret_value().encode(), password=None, backend=default_backend()
        )
        return value

    @cached_property
    def key(self):
        return serialization.load_pem_private_key(
            self._secret_value.encode(), password=None, backend=default_backend()
        )

    @cached_property
    def n(self):
        n = self.key.public_key().public_numbers().n
        return unsigned_int_to_urlsafe_b64(n)

    @cached_property
    def e(self):
        e = self.key.public_key().public_numbers().e
        return unsigned_int_to_urlsafe_b64(e)

    @cached_property
    def kid(self):
        return sha256(f"rsa:{self.e}:{self.n}".encode()).hexdigest()[:32]

    @cached_property
    def public_pem(self):
        return self.key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    @property
    def alg(self):
        return "RS256"

    @cached_property
    def jwk(self):
        return {
            "kid": self.kid,
            "kty": "RSA",
            "use": "sig",
            "alg": self.alg,
            "n": self.n,
            "e": self.e,
        }
