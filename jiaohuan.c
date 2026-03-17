#include <stdio.h>
int main()
{
	int a = 6;
	int b = 10;
	int c;
	printf("交换前:a=%d,b=%d\n", a, b);

	c = a;
	a = b;
	b = c;

	printf("交换后:a=%d,b=%d\n", a, b);
}