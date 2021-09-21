# RSA stream
Crypto, 100 points
## Description
```
I made a stream cipher out of RSA! But people say I made a huge mistake. Can you decrypt my cipher?
[Download](./rsa.tar.gz)
```

## Analysis
It encypt itself by xoring with encrypted flag with RSA. Each 256 bytes block, flag encrypted with different e.

## Solution
We can easily get encrypted flag with xoring `chal.py`. Those flags are encrypted with same n but different e.
Let's say we have two set (n, e_1, c_1), (n, e_2, c_2) and gcd(e_1, e_2) = 1(65537 and 65539 are both prime). With these two, we can get original message m by solving linear diophantine equation.

```
c_1 = m^e_1 mod n
c_2 = m^e_2 mod n
Find (a, b) s.t. ae_1 + be_2 = 1 mod n
c_1^a * c_2^b = m^(ae_1 + be_2) = m mod n
```

## Flag
`ACSC{changing_e_is_too_bad_idea_1119332842ed9c60c9917165c57dbd7072b016d5b683b67aba6a648456db189c}`
