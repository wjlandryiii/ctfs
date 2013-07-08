all: sc sc.bin

sc.bin: sc.o
	ld --oformat binary -T sc.lds -o sc.bin sc.o

sc: sc.o
	ld -T sc.lds -o sc sc.o

sc.o: sc.s
	as -o sc.o sc.s

clean:
	rm sc sc.bin sc.o

