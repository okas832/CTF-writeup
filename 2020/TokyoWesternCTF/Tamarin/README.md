# Tamarin

Apk that use Xamarin; app platform for building apps with .NET

## Road to find important routine

Jadx doesn't help me to find important routine from java files. Instead, found that this was build with Xamarin.

You can check them with decompress apk and check libraries in lib/armeabi-v7a/

There seems no dll file in the apk, but found the tool to extract DLL files from Xamarin apk.

https://github.com/tjg1/mono_unbundle

After extracting, we get the DLL file, Tamarin.dll, that contains the flag checking logic.

## Analysis

In namespace Core, there is a class Check.

In Func4, it gets string called flag, so we need to check it.

```C#
byte[] bytes = Encoding.ASCII.GetBytes(flag);
int length = flag.Length;
if ((length & 3) != 0)
	Array.Resize<byte>(ref bytes, length + (4 - (length & 3)));
for (int index = length; index < bytes.Length; ++index)
	bytes[index] = (byte) 0;
if (bytes.Length != Check.equations_arr.GetLength(0) * 4)
	return false;
```

First, it extend the flag length to make the length multiples of 4 with adding null.

```C#
List<List<uint>> uintListList = new List<List<uint>>();
for (int index1 = 0; index1 < Check.equations_arr.GetLength(0); ++index1)
{
	List<uint> uintList = new List<uint>();
	uintList.Add(BitConverter.ToUInt32(bytes, index1 * 4));
	for (int index2 = 0; index2 < Check.equations_arr.GetLength(1); ++index2)
		uintList.Add(Check.equations_arr[index1, index2]);
	uintListList.Add(uintList);
}
```

Split the flag with 4 bytes length, and put each them into first element of equations_arr's lists.

```C#
private static uint Func2(List<uint> coefficients, uint x, int pos) => pos == -1 ? 0U : coefficients[pos] * pow(x, pos) + Check.Func2(coefficients, x, pos - 1);

uint x = random_int();
for (int index = 0; index < 10000; ++index)
	x = Check.Func2(equation, x, equation.Count - 2);
checkResults.Add((int) x == (int) equation[equation.Count - 1]);
```

Writing the Func2 and below code to math formula

When,

![formula](https://render.githubusercontent.com/render/math?math=x_{0}=\textrm{random}())

![formula](https://render.githubusercontent.com/render/math?math=x_{j%2b1}=\sum^{31}_{i=0}%20\textrm{equation}[i]*{x_{j}}^{i}%20\mod%200\textrm{x}100000000)

should make ![formula](https://render.githubusercontent.com/render/math?math=x_{10000}) and  ![formula](https://render.githubusercontent.com/render/math?math=\textrm{equation}[32]) are same.

We know equation[1~32] and don't know equation[0] (our input).

## Solution

We've checked the random value ![formula](https://render.githubusercontent.com/render/math?math=x_{0}) cannot effects to ![formula](https://render.githubusercontent.com/render/math?math=x_{10000}).(By testing some random value and random equation[0])

One god came, rkm0959, look at the code and gives the solver that calculates equation[0] as fast as lighting.

```python
def solve(a):  # a is 32 length array, 
    x = a[32]
    t = a[32]
    for i in range(1, 32):
        t -= a[i] * pow(x, i, 2 ** 32)
    t = t % (2 ** 32)
    return t
```

It's a good guess to have ![formula](https://render.githubusercontent.com/render/math?math=a_{32}) as a "fixed point" of f, since iterations of f will stay at ![formula](https://render.githubusercontent.com/render/math?math=a_{32}) if we arrive there.
Therefore, we solve f(![formula](https://render.githubusercontent.com/render/math?math=a_{32})) =  ![formula](https://render.githubusercontent.com/render/math?math=a_{32}), which we can easily recover ![formula](https://render.githubusercontent.com/render/math?math=a_{0}) as ![formula](https://render.githubusercontent.com/render/math?math=a_{32}-\sum_{i=1}^{32}%20a_{i}{a_{32}}^{i})

Applying to all arrays to calculate flag...

```python
from Crypto.Util.number import long_to_bytes
a = [[2921822136,1060277104,2035740900,...],
     [...],
      ...
    ] # look at solver.py
 
def solve(a):
    x = a[32]
    t = a[32]
    for i in range(1, 32):
        t -= a[i] * pow(x, i, 2 ** 32)
    t = t % (2 ** 32)
    return t    

ans = b""
for i in a:
   ans += long_to_bytes(solve([0] + i))

print(b"TWCTF{" + ans + b"}")

```

And got it.

```
TWCTF{Xm4r1n_15_4bl3_70_6en3r4t3_N471v3_C0d3_w17h_VS_3n73rpr153_bu7_17_c0n741n5_D07_N3t_B1n4ry}
```
