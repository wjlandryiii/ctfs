#!/usr/bin/python

import socket
import re

TARGET = ("vuln1.quals.ructf.org", 16712)
#TARGET = ("ubuntu32vm", 16712)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(TARGET)

rxbuff = ""
for x in xrange(0, len("So, what do you think the flag is\n> ")):
    rxbuff += s.recv(1)

print rxbuff

s.sendall("@"*256)

rxbuff = ""
for x in xrange(0, len(" How pathetic. Here, have a hint:\n")):
    rxbuff += s.recv(1)

rxbuff = ""
chunk = s.recv(1024)
rxbuff += chunk
while len(chunk) > 0:
    chunk = s.recv(1024)
    rxbuff += chunk

print len(rxbuff)
print rxbuff


def decode(escstr, fg, bg):
    if escstr == "[0m":
        return 0, 7
    result = re.match(r"\[3([0-7])m", escstr)
    if result != None:
        return ord(result.group(1)) - ord('0'), bg
    result = re.match(r"\[4([0-7])m", escstr)
    if result != None:
        return fg, ord(result.group(1)) - ord('0')
    result = re.match(r"\[3([0-7]);4([0-7])m", escstr)
    return ord(result.group(1)) - ord('0'), ord(result.group(2)) - ord('0')

plaintext = ""
i = 0
fg = -1
bg = -1


while i < len(rxbuff):
    if(rxbuff[i] == "\x1B"):
        end = rxbuff.find("m", i)
        fg, bg = decode(rxbuff[i+1:end+1], fg, bg)
        i = end+1
    elif rxbuff[i] == '\n':
        i += 1
    else:
        #print fg, bg
        plaintext += chr((ord(rxbuff[i]) ^ ((bg << 3) | (fg))) & 0x3f)
        i += 1


print plaintext


s.close()