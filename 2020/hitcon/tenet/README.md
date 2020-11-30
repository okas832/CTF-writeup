# tenet

You have to start looking at the world in a new way

[server.rb](./server.rb)

[time_machine](./time_machine)

47 Teams solved.

## Binary summary

I can execute any assembly code.
But twice

1. Execute normally and records the rip.

2. Execute the record backward.

There is a 8byte random value on memory 0x2170000. And code cannot use stack memory.
When executing normally, code need to remove that random value and somehow save the random value.

Before executing backward, It checks if there are non-0 on 0x2170000 page and clean all the registers to 0.

And then execute backward. And saved random value needs to comeback at 0x2170000.

## Solution

We cannot use both register and memory. But we can save that data in indirect way to rip record.

First, we can make simple format for this.

```asm
    xor rcx, rcx
label:
    mov rdi, 0x2170000
    add rdi, rcx
    mov rbx, 0
    xchg bl, [rdi]
    sub rdi, rcx
    mov rdi, 0x2170008
	; do something to save and recover bl
    inc rcx
    cmp rcx, 8
    jne label
    mov rax, 0x3C
    syscall
```

Important part is to make "do something" part.

Easiest way to make it is, execute `inc bl`, `0x2170000[rcx]` times.

```asm
    lea rax, lable2
    mov rdx, 0xFF
    sub rdx, rbx   ; how many inc bl to pass
    add rdx, rdx   ; inc bl => 2byte instruction
    add rax, rdx
    jmp rax
lable2:
    inc bl
    inc bl
    ...
```
