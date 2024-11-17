import string
from typing import Dict
from hashlib import pbkdf2_hmac, sha512


class PasswordGenerator:
    def __init__(self, master_password: str, domain: str, username: str, length: str, salt: int):
        """
        Initializes the password generator with necessary parameters.

        Args:
            master_password (str): The master password for key derivation.
            domain (str): The domain or website for the password.
            username (str): The username associated with the password.
            salt (str): A salt for security.
            length (int): The desired length of the generated password.
        """
        self.master_password = master_password
        self.domain = domain
        self.username = username
        self.length = length
        self.salt = salt
        self.key = self._derive_key()
        del (self.master_password)

    def generate(self, special_characters: bool, lowercases: bool, uppercases: bool, digits: bool) -> str:
        """
        Generates a secure password based on the initialized parameters and character set options.

        Args:
            special_character (bool): Include special characters if True.
            lowercases (bool): Include lowercase letters if True.
            uppercases (bool): Include uppercase letters if True.
            digits (bool): Include digits if True.

        Returns:
            str: The generated password.
        """
        char_types = self._character_set({
            "punctuation": special_characters,
            "ascii_lowercase": lowercases,
            "ascii_uppercase": uppercases,
            "digits": digits
        })

        password = self._generate_initial_password(char_types)
        password = self._extend_password(password, char_types)
        password = self._shuffle_password(
            password, ''.join(char_types.values()))

        return password

    def _derive_key(self) -> int:
        """
        Derives a cryptographic key from the master password, domain, and username.

        Returns:
            int: A derived cryptographic key as an integer.
        """
        base_key = pbkdf2_hmac(
            "sha512", self.master_password, self.salt.encode("utf-8"), 100000)
        combined_data = f"{self.domain}{self.username}{self.length}".encode(
            "utf-8")
        derived_key = pbkdf2_hmac(
            "sha512", combined_data, base_key, 100000)
        return int.from_bytes(derived_key, "big")

    def _character_set(self, params: Dict[str, bool]) -> Dict[str, str]:
        """
        Generates a dictionary of character sets based on the specified flags.

        Args:
            params (Dict[str, bool]): Flags for including specific character sets (e.g., digits, lowercase).

        Returns:
            Dict[str, str]: A dictionary of character sets from the `string` module.
        """
        return {name: getattr(string, name) for name, include in params.items() if include}

    def _generate_initial_password(self, char_types: Dict[str, str]) -> str:
        """
        Generates a password using a derived key and specified character sets.

        Args:
            char_types (Dict[str, str]): The character sets to draw from.

        Returns:
            str: The generated password.
        """
        return ''.join(self.deterministic_choice(chars, self.key, type_name) for type_name, chars in char_types.items())

    def _extend_password(self, password: str, char_types: Dict[str, str]) -> str:
        """
        Extends the password to the desired length by adding characters deterministically.

        Args:
            password (str): The initial password.
            char_types (Dict[str, str]): Character sets to generate additional characters.

        Returns:
            str: The extended password.
        """
        return password + ''.join(self.deterministic_choice(''.join(char_types.values()), self.key, i) for i in range(len(password), self.length))

    def _shuffle_password(self, password: str, all_characters: str) -> str:
        """
        Shuffles the password characters deterministically using the key.

        Args:
            password (str): The password to shuffle.
            all_characters (str): All possible characters for the password.

        Returns:
            str: The shuffled password.
        """
        return ''.join(sorted(password, key=lambda x: self.deterministic_choice(all_characters, x, self.key)))

    @staticmethod
    def deterministic_choice(sequence: str, *args: str) -> str:
        """
        Selects a character from the sequence deterministically based on input arguments.

        Args:
            sequence (str): The character sequence to choose from.
            *args (str): Additional inputs that influence the choice.

        Returns:
            str: The selected character.
        """
        combined_input = ''.join(str(arg) for arg in args)
        hash_value = sha512(combined_input.encode()).hexdigest()
        index = int(hash_value, 16) % len(sequence)
        return sequence[index]
