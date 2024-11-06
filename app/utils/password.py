import hashlib
import base64
import re


def password_generator(
    master_password,
    domain,
    username,
    length,
    salt,
    special_character=True,
    remove_digits=False,
    remove_uppercase=False,
    digits_only=False,
):

    # Utiliser PBKDF2 pour dériver une clé sécurisée à partir du mot de passe principal et du salt
    derived_key = hashlib.pbkdf2_hmac(
        "sha512",
        master_password,
        salt.encode("utf-8"),
        100000,
    )

    # Effacer le mot de passe principal de la mémoire après avoir obtenu la clé dérivée
    master_password = None

    # Utiliser PBKDF2 avec la clé dérivée pour obtenir une clé pour la génération de mot de passe
    key = hashlib.pbkdf2_hmac(
        "sha512",
        f"{domain}{username}{length}".encode("utf-8"),
        derived_key,
        100000,
    )

    if special_character:
        encoded_data = base64.b85encode(key).decode("utf-8")
    else:
        encoded_data = base64.urlsafe_b64encode(key).decode("utf-8")
        encoded_data = encoded_data.replace("-", "")

    if remove_digits:
        encoded_data = re.sub(r"\d", "", encoded_data)

    if remove_uppercase:
        encoded_data = encoded_data.lower()

    if digits_only:
        encoded_data = re.sub(r"\D", "", encoded_data)

    password = encoded_data[:length]

    return password
