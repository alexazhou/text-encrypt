#ifdef BUILD_DLL 
	
/* DLL export */ 
	#define EXPORT __declspec (dllexport) 

#else /* EXE import */ 

	#define EXPORT __declspec (dllimport)

#endif 


EXPORT int __cdecl DES_Encrypt(char *plainFile, char *keyStr,char *cipherFile);
EXPORT int __cdecl DES_Decrypt(char *cipherFile, char *keyStr,char *plainFile);

EXPORT int __cdecl DES_Encrypt_Data(char *plainStr, char *keyStr,char *cipherStr,long int len);
EXPORT int __cdecl DES_Decrypt_Data(char *cipherStr, char *keyStr,char *plainStr,long int len);

