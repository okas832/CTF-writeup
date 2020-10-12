# trilemma

## Disassemble pyc

```python
import dis, marshal, sys

header_sizes = [
    (8,  (0, 9, 2)),
    (12, (3, 6)),
    (16, (3, 7)),
]
header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

with open("fixer.pyc", "rb") as f:
    metadata = f.read(header_size)
    code = marshal.load(f)

dis.dis(code)

```
[Source](https://stackoverflow.com/questions/32562163/how-can-i-understand-a-pyc-file-content)

## Analysis

The main part is easy to decompile by hand except lambda thing
```python
import read

s = input()
m = re.match('^SECCON{([A-Z]+)}$', s)
if not m:
	print('invalid flag')
else:
	s = m.group(1)
	f = lambda_thing...
	if f(s):
		print('correct')
	else:
		print('wrong')
return
```

Flag format is SECCON{<upper alphabet only>}.

### That lambda thing...
There are too many lambda here. To distinguish those, I'll label them.
```
Disassembly of <code object <lambda> at 0x0000012D71830710, file "fixer.py", line 9>:
  9           0 LOAD_CONST               1 (<code object <lambda> at 0x0000012D717F90E0, file "fixer.py", line 9>) = f1
              2 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
              4 MAKE_FUNCTION            0
              6 LOAD_CONST               3 (13611142019359843741091679554812914051545792465993098606064046040462991)
              8 CALL_FUNCTION            1
             10 LOAD_CONST               4 (<code object <lambda> at 0x0000012D7181D190, file "fixer.py", line 9>) = f2
             12 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
             14 MAKE_FUNCTION            0
             16 LOAD_CONST               5 (<code object <lambda> at 0x0000012D7181D710, file "fixer.py", line 9>) = f3
             18 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
             20 MAKE_FUNCTION            0
             22 CALL_FUNCTION            1
             24 LOAD_CONST               6 (<code object <lambda> at 0x0000012D718302F0, file "fixer.py", line 9>) = f4
             26 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
             28 MAKE_FUNCTION            0
             30 CALL_FUNCTION            1
             32 LOAD_CONST               4 (<code object <lambda> at 0x0000012D7181D190, file "fixer.py", line 9>) = f2
             34 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
             36 MAKE_FUNCTION            0
             38 LOAD_CONST               7 (<code object <lambda> at 0x0000012D71830500, file "fixer.py", line 9>) = f5
             40 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
             42 MAKE_FUNCTION            0
             44 CALL_FUNCTION            1
             46 LOAD_CONST               4 (<code object <lambda> at 0x0000012D7181D190, file "fixer.py", line 9>) = f2
             48 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
             50 MAKE_FUNCTION            0
             52 LOAD_CONST               8 (<code object <lambda> at 0x0000012D71830660, file "fixer.py", line 9>) = f6
             54 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>')
             56 MAKE_FUNCTION            0
             58 CALL_FUNCTION            1
             60 CALL_FUNCTION            1
             62 LOAD_FAST                0 (s)
             64 CALL_FUNCTION            1
             66 CALL_FUNCTION            1
             68 LOAD_CONST               9 (0)
             70 CALL_FUNCTION            1
             72 CALL_FUNCTION            1
             74 RETURN_VALUE
```
And decompile this using labels.
```python
def f0(s):  # It's function anyway 
	c = 13611142019359843741091679554812914051545792465993098606064046040462991
	return f1(c)(f2(f3)(f4)(f2(f5)(f2(f6))(s))(0))
```
We'll looke f2 first and analyze in this order
```
                               f2(f6)
                        f2(f5)(      )(s)
             f2(f3)(f4)(                 )(0)
return f1(c)(                                )
```
### f2
```
Disassembly of <code object <lambda> at 0x0000012D7181D190, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (a)
              2 BUILD_TUPLE              1
              4 LOAD_CONST               1 (<code object <lambda> at 0x0000012D7181D030, file "fixer.py", line 9>)
              6 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>')
              8 MAKE_FUNCTION            8 (closure)
             10 LOAD_CLOSURE             0 (a)
             12 BUILD_TUPLE              1
             14 LOAD_CONST               1 (<code object <lambda> at 0x0000012D7181D030, file "fixer.py", line 9>)
             16 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>')
             18 MAKE_FUNCTION            8 (closure)
             20 CALL_FUNCTION            1
             22 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D7181D030, file "fixer.py", line 9>:
  9           0 LOAD_DEREF               1 (a)
              2 LOAD_CLOSURE             0 (b)
              4 BUILD_TUPLE              1
              6 LOAD_CONST               1 (<code object <lambda> at 0x0000012D717F92F0, file "fixer.py", line 9>)
              8 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>')
             10 MAKE_FUNCTION            8 (closure)
             12 CALL_FUNCTION            1
             14 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D717F92F0, file "fixer.py", line 9>:
  9           0 LOAD_DEREF               0 (b)
              2 LOAD_DEREF               0 (b)
              4 CALL_FUNCTION            1
              6 LOAD_FAST                0 (c)
              8 CALL_FUNCTION            1
             10 RETURN_VALUE
```
We can decompile this,
```python
lambda a: (lambda b: a((lambda c: b(b)(c))))(lambda b: a((lambda c: b(b)(c))))
```
What's this? I will shortly explain

## Recursion with One argument first class function

You can see that,
```python
b(b) == (lambda b: a((lambda c: b(b)(c))))(lambda b: a((lambda c: b(b)(c))))
```
Let a returns lambda(that gets one any type of argument) and conditional branch depends on returned lambda's argument that calls a's argument or not.
```python
# easy example for a here
a = lambda rec: (lambda x: 0 if x == 0 else x + rec(x-1)) 
```
If a's return lambda takes argument as base case, it will not call anything and return some object.
If not, it'll call the a's argument with value of next step, same as ```b(b)(next_step_value)```, results ```a((lambda c: b(b)(c)))(next_step_value)```

So f2 can be called the function that helps to make recursive function. 

Thanks to KAIST CS320 Programming Language, I understand this function in 5 seconds when I was solving this challenge. 

## f2(f6)
```
Disassembly of <code object <lambda> at 0x0000012D71830660, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (a)
              2 BUILD_TUPLE              1
              4 LOAD_CONST               1 (<code object <lambda> at 0x0000012D718305B0, file "fixer.py", line 9>)
              6 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>')
              8 MAKE_FUNCTION            8 (closure)
			  10 RETURN_VALUE
			  
Disassembly of <code object <lambda> at 0x0000012D718305B0, file "fixer.py", line 9>:
  9           0 LOAD_FAST                0 (b)
              2 LOAD_CONST               1 (0)
              4 COMPARE_OP               2 (==)
              6 POP_JUMP_IF_FALSE       12
              8 LOAD_CONST               2 (1)
             10 RETURN_VALUE
        >>   12 LOAD_FAST                0 (b)
             14 LOAD_CONST               2 (1)
             16 BINARY_ADD
             18 LOAD_DEREF               0 (a)
             20 LOAD_FAST                0 (b)
             22 LOAD_CONST               2 (1)
             24 BINARY_SUBTRACT
             26 CALL_FUNCTION            1
             28 BINARY_MULTIPLY
             30 LOAD_CONST               3 (7)
             32 BINARY_ADD
             34 LOAD_CONST               4 (255)
             36 BINARY_AND
             38 RETURN_VALUE
```
is
```python
lambda a: (lambda b: 1 if b == 0 else ((b + 1) * a(b - 1) + 7) & 255
```
and f2(f6) is same with
```python
def f6(x):
	if x == 0:
		return 1
	return x + 1 * f6(x - 1) + 7 & 255

f6
```

## f2(f5)(f2(f6))(s)
```
Disassembly of <code object <lambda> at 0x0000012D71830500, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (f)
              2 BUILD_TUPLE              1
              4 LOAD_CONST               1 (<code object <lambda> at 0x0000012D71830450, file "fixer.py", line 9>)
              6 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>')
              8 MAKE_FUNCTION            8 (closure)
             10 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D71830450, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (b)
              2 LOAD_CLOSURE             1 (f)
              4 BUILD_TUPLE              2
              6 LOAD_CONST               1 (<code object <lambda> at 0x0000012D718303A0, file "fixer.py", line 9>)
              8 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>')
             10 MAKE_FUNCTION            8 (closure)
             12 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D718303A0, file "fixer.py", line 9>:
  9           0 LOAD_GLOBAL              0 (len)
              2 LOAD_FAST                0 (c)
              4 CALL_FUNCTION            1
              6 LOAD_CONST               1 (0)
              8 COMPARE_OP               2 (==)
             10 POP_JUMP_IF_FALSE       16
             12 BUILD_LIST               0
             14 RETURN_VALUE
        >>   16 LOAD_DEREF               0 (b)
             18 LOAD_GLOBAL              1 (ord)
             20 LOAD_FAST                0 (c)
             22 LOAD_CONST               1 (0)
             24 BINARY_SUBSCR
             26 CALL_FUNCTION            1
             28 LOAD_CONST               2 (65)
             30 BINARY_SUBTRACT
             32 CALL_FUNCTION            1
             34 BUILD_LIST               1
             36 LOAD_DEREF               1 (f)
             38 LOAD_DEREF               0 (b)
             40 CALL_FUNCTION            1
             42 LOAD_FAST                0 (c)
             44 LOAD_CONST               3 (1)
             46 LOAD_CONST               0 (None)
             48 BUILD_SLICE              2
             50 BINARY_SUBSCR
             52 CALL_FUNCTION            1
             54 BINARY_ADD
             56 RETURN_VALUE
```
is
```python
lambda f: (lambda b: (lambda c: [] if len(c) == 0 else [b(ord(c[0]) - 65)] + f(b)(c[1:])
# f : for make recursion
# b : f2(f5)'s argument(will be f2(f6))
# c : recursion step value
```
and f2(f5) is same with
```python
def f5(f):
	def f5_1(x):
		if len(x) == 0:
			return []
		return f(ord(x[0] - 65)) + f5_1(c[1:])
	return f5_1
	
f5
```
and f2(f5)(f2(f6))(s) results
```python
def f6(x):
	if x == 0:
		return 1
	return x + 1 * f6(x - 1) + 7 & 255

def f5(x):
	if len(x) == 0:
		return []
	return f6(ord(x[0] - 65)) + f5(c[1:])
	
f5(s)
```

## f2(f3)(f4)(f2(f5)(f2(f6))(s))(0)
For f4,
```
Disassembly of <code object <lambda> at 0x0000012D718302F0, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (a)
              2 BUILD_TUPLE              1
              4 LOAD_CONST               1 (<code object <lambda> at 0x0000012D71830240, file "fixer.py", line 9>)
              6 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>')
              8 MAKE_FUNCTION            8 (closure)
             10 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D71830240, file "fixer.py", line 9>:
  9           0 LOAD_DEREF               0 (a)
              2 LOAD_CONST               1 (<code object <lambda> at 0x0000012D71820870, file "fixer.py", line 9>)  # same with f2
              4 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>')
              6 MAKE_FUNCTION            0
              8 LOAD_CONST               3 (<code object <lambda> at 0x0000012D71830190, file "fixer.py", line 9>)  # f7
             10 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>')
             12 MAKE_FUNCTION            0
             14 CALL_FUNCTION            1
             16 LOAD_FAST                0 (b)
             18 CALL_FUNCTION            1
             20 BINARY_MULTIPLY
             22 LOAD_FAST                0 (b)
             24 BINARY_ADD
             26 RETURN_VALUE
```
is
```python
lambda a: lambda b: a * f2(f7)(b) + b
```
and same with
```python
def f4(a, b):  # chaining lambda f4(a)(b) == f4(a, b)
	return a * f7(b) + b
```

For f7,
```
Disassembly of <code object <lambda> at 0x0000012D71830190, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (a)
              2 BUILD_TUPLE              1
              4 LOAD_CONST               1 (<code object <lambda> at 0x0000012D718300E0, file "fixer.py", line 9>)
              6 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>')
              8 MAKE_FUNCTION            8 (closure)
             10 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D718300E0, file "fixer.py", line 9>:
  9           0 LOAD_FAST                0 (b)
              2 LOAD_CONST               1 (266)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE       16
              8 LOAD_FAST                0 (b)
             10 LOAD_CONST               2 (10)
             12 BINARY_SUBTRACT
             14 RETURN_VALUE
        >>   16 LOAD_DEREF               0 (a)
             18 LOAD_DEREF               0 (a)
             20 LOAD_FAST                0 (b)
             22 LOAD_CONST               3 (11)
             24 BINARY_ADD
             26 CALL_FUNCTION            1
             28 CALL_FUNCTION            1
             30 RETURN_VALUE
```
is
```python
lambda a: lambda b: b - 10 if b > 266 else a(a(b+11))
```
and f2(f7) is same as
```python
def f7(x):  # always return 257, But IDK why
	if x > 266:
		return x - 10
	return f7(f7(x + 11))
```

For f2(f3),
```
Disassembly of <code object <lambda> at 0x0000012D7181D710, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (f)
              2 BUILD_TUPLE              1
              4 LOAD_CONST               1 (<code object <lambda> at 0x0000012D7181D5B0, file "fixer.py", line 9>)
              6 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>')
              8 MAKE_FUNCTION            8 (closure)
             10 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D7181D5B0, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             0 (b)
              2 LOAD_CLOSURE             1 (f)
              4 BUILD_TUPLE              2
              6 LOAD_CONST               1 (<code object <lambda> at 0x0000012D7181D450, file "fixer.py", line 9>)
              8 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>')
             10 MAKE_FUNCTION            8 (closure)
             12 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D7181D450, file "fixer.py", line 9>:
  9           0 LOAD_CLOSURE             1 (b)
              2 LOAD_CLOSURE             0 (c)
              4 LOAD_CLOSURE             2 (f)
              6 BUILD_TUPLE              3
              8 LOAD_CONST               1 (<code object <lambda> at 0x0000012D7181D2F0, file "fixer.py", line 9>)
             10 LOAD_CONST               2 ('<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>.<locals>.<lambda>')
             12 MAKE_FUNCTION            8 (closure)
             14 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000012D7181D2F0, file "fixer.py", line 9>:
  9           0 LOAD_GLOBAL              0 (len)
              2 LOAD_DEREF               1 (c)
              4 CALL_FUNCTION            1
              6 LOAD_CONST               1 (0)
              8 COMPARE_OP               2 (==)
             10 POP_JUMP_IF_FALSE       16
             12 LOAD_FAST                0 (d)
             14 RETURN_VALUE
        >>   16 LOAD_DEREF               0 (b)
             18 LOAD_DEREF               2 (f)
             20 LOAD_DEREF               0 (b)
             22 CALL_FUNCTION            1
             24 LOAD_DEREF               1 (c)
             26 LOAD_CONST               2 (1)
             28 LOAD_CONST               0 (None)
             30 BUILD_SLICE              2
             32 BINARY_SUBSCR
             34 CALL_FUNCTION            1
             36 LOAD_FAST                0 (d)
             38 CALL_FUNCTION            1
             40 CALL_FUNCTION            1
             42 LOAD_DEREF               1 (c)
             44 LOAD_CONST               1 (0)
             46 BINARY_SUBSCR
             48 CALL_FUNCTION            1
             50 RETURN_VALUE
```
is
```python
lambda f: (lambda b: (lambda c: (lambda d: d if len(c) == 0 else b(f(b)(c[1:])(d))(c[0]))))
# f : for make recursion
# b : f2(f3)'s argument(== f4)
# c : f2(f3)(f4)'s argument(== f2(f5)(f2(f6))(s))
# d : start value
```
So f2(f3) is,
```
def f3(b):
	def f3_1(c, d):
		if len(c) == 0:
			return 0
		return b(f3_1(c[1:], d), c[0])
	return f3_1
f3
```
and f2(f3)(f4)(f2(f5)(f2(f6))(s))(0) is
```python

def f7(x):
	if x > 266:
		return x - 10
	return f7(f7(x + 11))

def f6(x):
	if x == 0:
		return 1
	return x + 1 * f6(x - 1) + 7 & 255

def f5(x):
	if len(x) == 0:
		return []
	return f6(ord(x[0] - 65)) + f5(c[1:])

def f4(a, b):
	return a * f7(b) + b

def f3(c, d):
	if len(c) == 0:
		return 0
	return f4(f3(c[1:], d), c[0])
	
f3(f5(s), 0)
```

f1 is simple,
```python
f3(f5(s), 0) == 13611142019359843741091679554812914051545792465993098606064046040462991
```

## Solution
f5 changes each letter to some value and wrap with list, and f3 gets a list and encode to base257.
Input is just upper case letter, so we can make f5's table.
After decoding base257 and subtitude each digit with f5 table, we can get a flag.

```python
b = 13611142019359843741091679554812914051545792465993098606064046040462991
def calc(x):
    if x == 0:
            return 1
    return ((x + 1) * a(x-1) + 7) & 0xFF

lst = []
for i in range(26):
    lst.append(calc(i))

ans = ""
while b:
    ans += chr(lst.index(b % 257) + 65)
    b //= 257

print("SECCON{" + ans + "}")
```

## ETC
There is easy way to extract the encoded value by adding _PyObject_Dump at COMPARE_OP handler. We can guess that it's base257 by changing one letter from input. (차현수's solution)
We solved this in two ways at the same time, and got first blood anyway.