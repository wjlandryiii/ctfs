RoboAuth
========
## Category: Reversing

This is a Windows 32-bit crackme.  

It had two stages.  The first stage was simple.  The password could be recovered by debugging and checking the parameters to strcmp().

The second stage will XOR each byte of the second password with the key 0x2, and then compare the result with the string "u1nnf2lg".  To recover the password, XOR each byte of the string "u1nnf2lg" with 0x2.  The result is "w3lld0ne".

The code for the second stage was in an exception handler that would only be triggered if the process was not being debugged.  This was accomplished by calling AddVectoredExceptionHandler(1, 0x40157f) then execute an int 0x3 (invoke debugger).  When the process is being debugged, the debugger handles the exception just as it would with any breakpoint.  When the process is run without a debugger, the kernel triggers the registered exception handler at 0x40157f that contains the rest of the code for the crackme.
