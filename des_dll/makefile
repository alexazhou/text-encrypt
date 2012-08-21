all: des_demo.exe

des_demo.exe : des_demo.o des_X2.dll
	gcc -o des_demo.exe des_demo.o des_X2.dll

des_demo.o: des_demo.c des.h
	gcc -c des_demo.c

des_X2.dll: des_X2.o
	gcc -shared -o des_X2.dll des_X2.o -WL
	
des_X2.o : des_X2.c des.h
	gcc -c -DBUILD_DLL des_X2.c
	
clean:
	rm 2.txt 3.txt des_demo.exe des_demo.o des_X2.dll des_X2.o