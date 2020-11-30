#include<stdio.h>

void f(unsigned int a, unsigned int b, unsigned int c, unsigned int d, unsigned int e, unsigned int x1, unsigned int x2)
{
	unsigned int k = e * 0x20;
	int i;
	for (i = 0; i < 32; i++)
	{
		x2 = x2 - (((x1 << 0x4) + c) ^ ((x1 >> 0x5) + d) ^ (x1 + k));
		x1 = x1 - (((x2 << 0x4) + a) ^ ((x2 >> 0x5) + b) ^ (x2 + k));
		k -= e;
	}
	printf("%c%c%c%c%c%c%c%c",  *(((char*)&x1) + 0),
		                        *(((char*)&x1) + 1),
								*(((char*)&x1) + 2),
								*(((char*)&x1) + 3),
								*(((char*)&x2) + 0),
								*(((char*)&x2) + 1),
								*(((char*)&x2) + 2),
								*(((char*)&x2) + 3)
		);
}

int main()
{
	f(0x69a33fff, 0x468932dc, 0x2b0b575b, 0x1e8b51cc, 0x51fdd41a, 0x152ceed2, 0xd6046dc3);
	f(0x32e57ab6, 0x7785df55, 0x688620f9, 0x8df954f3, 0x5c37a6db, 0x4a9d3ffd, 0xbb541082);
	f(0xaca81571, 0x2c19574f, 0x1bd1fc38, 0x14220605, 0xb4f0b4fb, 0x632a4f78, 0xa9cb93d);
	f(0x33f33fe0, 0xf9de7e36, 0xe9ab109d, 0x8d4f04b2, 0xd3c45f8c, 0x58aae351, 0x92012a14);
	return 0;
}