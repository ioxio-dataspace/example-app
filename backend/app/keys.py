import json
import textwrap
from base64 import urlsafe_b64decode, urlsafe_b64encode
from functools import cached_property
from hashlib import sha256

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
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
    private_key: RSAPrivateKey

    def __init__(self, value: str) -> None:
        value = textwrap.dedent(value).strip()
        super().__init__(value)
        self.private_key = self._load_and_validate_key(value)

    @staticmethod
    def _load_and_validate_key(value: str) -> RSAPrivateKey:
        """
        Load and validate the RSA private key.

        :return: The RSAPrivateKey object.
        """
        key = serialization.load_pem_private_key(
            value.encode(), password=None, backend=default_backend()
        )
        return key

    def __repr__(self) -> str:
        return f"RsaPrivateKey('{self}')"

    @property
    def public_key(self) -> RSAPublicKey:
        return self.private_key.public_key()

    @cached_property
    def n(self) -> str:
        n = self.public_key.public_numbers().n
        return unsigned_int_to_urlsafe_b64(n)

    @cached_property
    def e(self) -> str:
        e = self.public_key.public_numbers().e
        return unsigned_int_to_urlsafe_b64(e)

    @cached_property
    def kid(self) -> str:
        """
        JSON Web Key (JWK) Thumbprint of the key (see RFC 7638).
        """
        json_object = json.dumps(
            {
                "kty": self.kty,
                "n": self.n,
                "e": self.e,
            },
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        raw_hash = sha256(json_object).digest()
        return urlsafe_b64encode(raw_hash).decode().rstrip("=")

    @cached_property
    def public_pem(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    @property
    def alg(self) -> str:
        return "RS256"

    @property
    def kty(self) -> str:
        return "RSA"

    @cached_property
    def jwk(self) -> dict[str, str]:
        return {
            "kid": self.kid,
            "kty": self.kty,
            "use": "sig",
            "alg": self.alg,
            "n": self.n,
            "e": self.e,
        }
