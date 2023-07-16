# topology

No worries. It's a network topology, not an algebraic one.

[topology](./topology)

30 Teams solved.

## Solution

It fork into 99 process and those 99 process will check blocks (each block length is 8 bytes) of our input.

After every process check the block of input. More than 4 processes need to agree that the input is correct. 

Functions with random 8 letter have a validation logic for each processes and those are reversable. 

After solving them, we can get a flag by collecting the most common answers.

## Notes of solve.py

My solve.py is not perfect but produces correct answer.

Maybe finding only "cmp  rax, rdx" for finding validation basic block is a problem.

## Flag

`zer0pts{kMo7UtDhqMfXhaUp0kP8MEPLPJFgKUx7YlWyyxB9POKUhegFqdNm5sXIfxk2FIfV}`