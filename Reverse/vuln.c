#include <stdio.h>
int main()
{
	char buf[100];
	char flag[16];
	int super_secret_array[] = {1,3,}



	memset(buf,0x00,sizeof(buf)); 
	for(int i=0;i<100;i++)
      scanf("%d", &buf[i]);
    strcpy(flag, buf);
    printf("%d\n", buf );
}


