Pay TV
======

## (Category: Web)


target: <https://ctf.fluxfingers.net:1316/>

You have to find the password to watch tv.

The password is posted through AJAX to <https://ctf.fluxfingers.net:1316/gimmetv> and returns a JSON object.
The javascript that handles the AJAX request contains a clue:

```
xhr.send('key=' + encodeURIComponent(key)/* + '&debug'*/)
```

If you include the `&debug` parameter, the returned JSON object will include how long it took the server to process the request.

Without `debug`:

```
{"response": "Wrong key.", "success": false}
```

With `debug`:

```
{"start": 1382646442.585405, "end": 1382646442.585503, "response": "Wrong key.", "success": false}
```

The service is vulnerable to a [timing attack](http://en.wikipedia.org/wiki/Timing_attack>).  The password can be recovered by guessing one character at a time, and compairing the times of each guess.  The guess that took the longest time is likely correct.

