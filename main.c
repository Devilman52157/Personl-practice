#include <stdio.h>
int main()
{
	int a;
	int b;

	printf("请输入两个数字：");
	scanf_s("%d %d", &a, &b);

	double c = (a+b) / 2.0;

	printf("% d 和 % d 的平均值 =%f\n", a, b, c);
}