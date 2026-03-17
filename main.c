#include <stdio.h>
int main()
{
	int hour1, minute1;
	int hour2, minute2;

	printf("请输入时间:(小时 分)");
	scanf_s("%d %d", &hour1, &minute1);
	printf("请输入时间:(小时 分)");
	scanf_s("%d %d", &hour2, &minute2);

	int t1 = hour1 * 60 + minute1;
	int t2 = hour2 * 60 + minute2;

	int t = t1 - t2;

	if (t < 0)
		t = -t;

	printf("时差是%d小时%d分", t / 60, t % 60);

	return 0;
}