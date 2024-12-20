import base64
import math
import secrets
from collections.abc import Sequence

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.hashes import HashAlgorithm
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pwdlib.hashers import HasherProtocol
from pwdlib.hashers.argon2 import Argon2Hasher as Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher as BcryptHasher

from pydentity.utils import ensure_str, ensure_bytes

__all__ = (
    "Argon2Hasher",
    "BcryptHasher",
    "PBKDF2Hasher",
)

RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_random_string(length: int, allowed_chars: Sequence[str] = RANDOM_STRING_CHARS) -> str:
    return "".join(secrets.choice(allowed_chars) for _ in range(length))


def must_update_salt(salt: str, expected_entropy: int) -> bool:
    return len(salt) * math.log2(len(RANDOM_STRING_CHARS)) < expected_entropy


class PBKDF2Hasher(HasherProtocol):
    salt_entropy: int = 128

    __slots__ = (
        "_algorithm",
        "_hash_len",
        "_iterations",
    )

    def __init__(
        self,
        algorithm: HashAlgorithm = hashes.SHA256(),
        hash_len: int = 32,
        iterations: int = 720000,
    ):
        self._algorithm = algorithm
        self._hash_len = hash_len
        self._iterations = iterations

    def _generate_salt(self) -> str:
        char_count = math.ceil(self.salt_entropy / math.log2(len(RANDOM_STRING_CHARS)))
        return get_random_string(char_count, allowed_chars=RANDOM_STRING_CHARS)

    @classmethod
    def identify(cls, hash: str | bytes) -> bool:
        return ensure_str(hash).startswith("$pbkdf2$")

    def hash(
        self,
        password: str | bytes,
        *,
        salt: bytes | None = None,
    ) -> str:
        if salt and "$" in ensure_str(salt):
            raise ValueError("salt must be provided and cannot contain $.")

        salt = salt or ensure_bytes(self._generate_salt())
        pbkdf2 = PBKDF2HMAC(
            algorithm=self._algorithm,
            length=self._hash_len,
            salt=salt,
            iterations=self._iterations,
        )
        hash = base64.b64encode(pbkdf2.derive(ensure_bytes(password)))
        return "$pbkdf2$%s$%d$%s$%s" % (
            self._algorithm.name,
            self._iterations,
            ensure_str(salt),
            ensure_str(hash),
        )

    def verify(
        self,
        password: str | bytes,
        hash: str | bytes,
    ) -> bool:
        algorithm, iterations, salt, _hash = ensure_str(hash).removeprefix("$pbkdf2$").split("$", 3)
        pbkdf2 = PBKDF2HMAC(
            algorithm=self._algorithm,
            length=self._hash_len,
            salt=ensure_bytes(salt),
            iterations=int(iterations),
        )
        try:
            pbkdf2.verify(ensure_bytes(password), base64.b64decode(_hash))
            return True
        except InvalidKey:
            return False

    def check_needs_rehash(self, hash: str | bytes) -> bool:
        algorithm, iterations, salt, _hash = ensure_str(hash).removeprefix("$pbkdf2$").split("$", 3)
        update_salt = must_update_salt(salt, self.salt_entropy)
        return (int(iterations) != self._iterations) or update_salt
