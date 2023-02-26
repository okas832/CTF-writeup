#include<stdio.h>
#include<stdlib.h>
unsigned int seed = 0x3D2964F0;

unsigned int rand()
{
    unsigned int v1 = seed & 1;
    seed >>= 1;
    seed ^= v1 * 0x80200003;
    return seed;
}
char d[] = { 0x1, 0x19, 0xEF, 0x5A, 0xFA, 0xC8, 0x2E, 0x69, 0x31, 0xD7, 0x81, 0x21 };
int main()
{
    unsigned int* arr;
    unsigned long long int i;
    arr = calloc(1, 0x100000001 * sizeof(int));
    arr[0] = 0x3D2964F0;
    for(i = 1; i <= 0x100000000; i++)
    {
        arr[i] = rand();
    }
    unsigned long long int v = 1;
    unsigned long long int s = 0;

    for (i = 0; i <= 11; i++)
    {
        s += v;
        s %= 0xFFFFFFFF;
        printf("%c", d[i] ^ ((arr[s]) & 0xFF));
        v *= 42;
    }
    
    printf("\n");
    free(arr);
    return 0;
}