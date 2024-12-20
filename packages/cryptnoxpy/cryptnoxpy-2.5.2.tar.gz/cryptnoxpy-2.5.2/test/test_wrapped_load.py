# Copyright (c) 2020  Cryptnox SA 36 Avenue Cardinal Mermillod 1227 Carouge - Switzerland

# All Rights Reserved

# No part of this software or any of its contents may be reproduced, copied, modified or adapted, 
# without the prior written consent of the owner, unless otherwise indicated for stand-alone materials. 

# Commercial use and distribution of the contents of the software is not allowed 
# without express and prior written consent of the owner.
"""
This script sets up a cryptographic card, generates an RSA seed wrapper, encrypts a seed with the RSA wrapper, 
and loads the encrypted seed onto the card.
Functions:
    random_bytes(nlen: int) -> bytes:
    setup_logger() -> logging.Logger:
    get_card() -> BasicG1:
    setup_card() -> BasicG1:
    build_rsa_wrapper(response_bytes: bytes) -> rsa.RSAPublicKey:
Main Execution:
    - Sets up the card.
    - Generates an RSA seed wrapper.
    - Extracts the modulus and builds the RSA wrapper from the response.
    - Encrypts the seed with the RSA wrapper.
    - Loads the encrypted seed onto the card.
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptnoxpy.card.basic_g1 import BasicG1
from datetime import datetime

from mnemonic import Mnemonic
import cryptnoxpy as cp
import logging

EASY_MODE_PIN = "000000000"
EASY_MODE_PUK = "000000000000"

def generate_bip39_seed(mnemonic_words: str, passphrase: str = "") -> bytes:
    """
    Generate a BIP39 seed from a given mnemonic phrase and optional passphrase.

    Args:
        mnemonic_words (str): The mnemonic phrase (BIP39 words).
        passphrase (str): An optional passphrase to use for seed generation.

    Returns:
        bytes: A bytes object containing the generated BIP39 seed.
    """
    mnemo = Mnemonic("english")
    return mnemo.to_seed(mnemonic_words, passphrase)

# Example mnemonic phrase (replace with your own)
mnemonic_words = "achieve advance benefit create develop enhance improve inspire progress succeed thrive vision"
seed = generate_bip39_seed(mnemonic_words)

def setup_logger() -> logging.Logger:
    """
    Sets up a logger with a custom formatter.
    The custom formatter formats the log messages to include the current date and time
    in the format "dd-MMM-YYYY_hh:mmAM/PM", followed by the log level and the message.
    Returns:
        logging.Logger: A configured logger instance with a stream handler and custom formatting.
    """
    class CustomFormatter(logging.Formatter):
        def formatTime(self, record, datefmt=None):
            return datetime.now().strftime("%d-%b-%Y_%I:%M%p")

    formatter = CustomFormatter(fmt='%(asctime)s_%(levelname)s--%(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    return logger

logger = setup_logger()

def get_card() -> BasicG1:
    """
    Retrieves a card instance using the factory method and establishes a new connection.
    
    This function is used to get the card and refresh the card session when necessary for further operations.
    
    Returns:
        BasicG1: An instance of the card.
    """
    return cp.factory.get_card(cp.Connection())

def setup_card() -> BasicG1:
    """
    Sets up a card by initializing or resetting it.
    This function retrieves a card and checks if it is initialized. If the card is already initialized,
    it resets the card using the provided PUK (Personal Unblocking Key) and retrieves the card again.
    If the card is not initialized, it initializes the card with the provided name, email, PIN, and PUK,
    and retrieves the card again.
    Returns:
        BasicG1: The initialized or reset card.
    """
    card = get_card()

    if card.initialized:
        logger.info("Card is initialized. Resetting card.")
        card.reset(EASY_MODE_PUK)
        card = get_card()

    if not card.initialized:
        logger.info("Card is not initialized. Setting up card.")
        card.init(
            name="EASY MODE",
            email="easy@mode.com",
            pin=EASY_MODE_PIN,
            puk=EASY_MODE_PUK
        )
        card = get_card()
    
    return card

def build_rsa_wrapper(response_bytes: bytes) -> rsa.RSAPublicKey:
    """
    Constructs an RSA public key from a given byte sequence.

    Args:
        response_bytes (bytes): A byte sequence containing the RSA modulus prefixed with "CRSA".

    Returns:
        rsa.RSAPublicKey: An RSA public key object.

    Explanation:
        - The modulus is extracted from the response bytes.
        - The "CRSA" prefix is skipped (length of 4 bytes), so the modulus starts immediately after.
        - The modulus size is determined based on the RSA key size (e.g., 2048 bits).
          - RSA key size in bytes = modulus size in bits // 8.
          - For a 2048-bit RSA key, the modulus size is 256 bytes.
        - `modulus_end` is calculated as the modulus size (256 bytes) plus 4 bytes for the "CRSA" prefix.

        - The exponent is fixed at `0x10001` (65537), which is a widely used public exponent in RSA
          due to its balance between security and computational efficiency.

    Raises:
        ValueError: If the byte sequence does not contain a valid modulus.
    """
    modulus_start = len("CRSA")  # Skip the "CRSA" prefix
    modulus_end = 2048 // 8 + 4  # Modulus size (256 bytes for 2048-bit RSA) + 4 bytes for prefix
    modulus = int.from_bytes(response_bytes[modulus_start:modulus_end], byteorder='big')
    exponent = 65537  # Fixed public exponent (0x10001)
    return rsa.RSAPublicNumbers(exponent, modulus).public_key(default_backend())


if __name__ == "__main__":
    logger.info("Setting up card.")
    card = setup_card()

    logger.info("Generating RSA seed wrapper.")
    response_bytes = card.generate_seed_wrapper()

    logger.info("Extracting modulus and building RSA wrapper from response.")
    rsa_seed_wrapper = build_rsa_wrapper(response_bytes)

    logger.info("Encrypting seed with RSA wrapper.")
    wrapped_seed = rsa_seed_wrapper.encrypt(
        seed,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA1()), algorithm=hashes.SHA1(), label=None
        )
    )

    logger.info("Loading encrypted seed onto card.")
    card.load_wrapped_seed(wrapped_seed, EASY_MODE_PIN)
