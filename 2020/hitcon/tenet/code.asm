xor rcx, rcx
mov rdi, 0x2170000
add rdi, rcx
mov rbx, 0
xchg bl, [rdi]
sub rdi, rcx
mov rdi, 0x2170008
lea rax, [rip+0x10]
mov rdx, 0xFF
sub rdx, rbx
add rdx, rdx
add rax, rdx
jmp rax
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc bl
inc rcx
cmp rcx, 8
jne $-0x23B
mov rax, 0x3C
syscall