#include <stdio.h>
#include <string.h>


int main(){
char secret_array[16];
printf("Input password: ");
scanf("%s",secret_array);
if (strcmp(secret_array,"flag{e4sy_C_language}")==0){printf("Congratulations!\n");}
else {
printf("Ne polushilos, ne fortanulo\n");}
return 0;

}

