##
## EPITECH PROJECT, 2019
## 103cipher_2019
## File description:
## cryptage.py
##

import sys
import math

def encrypt(key_matrix, message_matrix):
    output_matrix = message_matrix * key_matrix
    separator = " "
    return separator.join(str(v) for v in output_matrix.values())

def decrypt(key_matrix, message_matrix):
    output_matrix = message_matrix * key_matrix
    separator = ""
    try:
        return separator.join(chr(round(v)) for v in output_matrix.values() if round(v) != 0)
    except ValueError:
        sys.exit(84)
