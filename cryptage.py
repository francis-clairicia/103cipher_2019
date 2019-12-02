##
## EPITECH PROJECT, 2019
## 103cipher_2019
## File description:
## crypt.py
##

import math

def encrypt(key_matrix, message_matrix):
    output_matrix = message_matrix * key_matrix
    output = ""
    for coord in output_matrix.coords():
        output += str(output_matrix[coord])
        output += " "
    return "Encrypted", output[:-1]

def decrypt(key_matrix, message_matrix):
    output_matrix = message_matrix * key_matrix
    output = ""
    for coord in output_matrix.coords():
        output += chr(round(output_matrix[coord]))
    return "Decrypted", output[:-1]
