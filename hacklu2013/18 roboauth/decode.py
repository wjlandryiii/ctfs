#!/usr/bin/python

def decode_str(cipher, key):
	plain_text = ""
	for x in cipher:
		plain_text += chr(ord(x)^key)
	return plain_text

print decode_str("u1nnf2lg", 2)
