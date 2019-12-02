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
    output = ""
    for coord in output_matrix.coords():
        output += str(output_matrix[coord])
        output += " "
    return output[:-1]

def decrypt(key_matrix, message_matrix):
    output_matrix = message_matrix * key_matrix
    output = ""
    for coord in output_matrix.coords():
        try:
            value = round(output_matrix[coord])
            if value != 0:
                output += chr(value)
        except ValueError:
            sys.exit(84)
    return output
