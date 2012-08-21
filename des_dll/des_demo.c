#include <stdio.h>
#include <memory.h>  
#include <time.h>
#include <stdlib.h>  

#include "des.h"

int main()  
{     
	clock_t a,b;  
	char *key = "ABCDEFGH12345678";
	
	a = clock();  
	DES_Encrypt("1.txt",key,"2.txt");  
	b = clock();  
	printf("º”√‹œ˚∫ƒ%d∫¡√Î\n",b-a);  
	  
	system("pause");  
	a = clock();  
	DES_Decrypt("2.txt",key,"3.txt");  
	b = clock();  
	printf("Ω‚√‹œ˚∫ƒ%d∫¡√Î\n",b-a);  
	getchar(); 
	
	char tmp[100] ={0};
	char tmp_2[100] ={0};

	char *plainStr = "12345678abcdefgh1";
	long int n_plain,n_cipher = 0;

	DES_Encrypt_Data(plainStr,key,tmp,16);
	printf("data len is %d\n",n_cipher);

	
	DES_Decrypt_Data(tmp, key,tmp_2,16);
	
	printf("data decrypted is %s\n",tmp_2);
	

	getchar(); 
	
	return 0;  
}   
