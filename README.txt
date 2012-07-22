
Deitel's How to Program books (Java, C++, C#) have a couple exercises to emulate
the other aspects of the programming environment. The first example is the VM that
they call Simpletron. To incentivize learning Python, I am implemented it. The second
exercise involves creating a BASIC-esque compiler to generate its machine code. The
complete version is tagged as '1.0' subsequent commits (& branches?) reflect optional
improvements to the pair.

SIMPLETRON ISA:

Accumulator, IR, PC; RAM of 100 integers. Advanced adds an index register.

	READ = 10xx
	WRITE = 11xx
	LOAD = 20xx
	STORE = 21xx
	ADD = 30xx
	SUBTRACT = 31xx
	DIVIDE = 32xx
	MULTIPY = 33xx
	MODULUS = 34xx
	BRANCH = 40xx
	BRANCHNEG = 41xx
	BRANCHZERO = 42xx
	HALT = 43xx (also 0)

xx is the address of the value to operate on. The math operations use the directed
value on whatever is in the accumulator.

SIMPLE COMPILER GRAMMER:

A: D X | D C E | D I E G D
C: rem | input | let | print
D: { 0-9 } | DD
E: L | D | L O D | L O E
G: goto
I: if
L: { a-z } | LL
O: + | - | * | / | % | = | > | < | ==
X: end

It has been a long time, and rewriting this grammer became tedious, but I think
that conforms. The point is that a line involves [line number] [command] [expression]
following the forms that the commands demand.

SIMPLE COMMANDS

rem "" - commented string
input x - value from terminal
let x = ( 5 + 3 ) / 2 - assign via x = expression
print 5 - print to terminal
goto 6 - unconditional jump
if 5 >= n goto 3 - conditional jump, form of if [ expression ] goto [ line number ]
end - stop execution

ADVANCED COMMANDS
for x = 10 to 50 step 10
[statements]
next ## signals end

def function ## definition
[statements; no args, all vars global]
return
gosub function ## usage

array tab = 5, 3, 6
array tub[5]
tab.len ## = 3
tub[4] ## zero index, of course

RUNNING INSTRUCTIONS

(written for Python 2.6.7; Py 3.x need to alter prints and so on) 
To test cpu alone, uncomment comp needs lines 7 & 37 to read from the command line
and then use "comp.py [filename]".
To test the compiler use "testCompiler.py [filename]". It will ask whether you want
to run the file; any answer with y in it will run the .sml file through simpletron.
Simpletron is currently set to verbose in comp, flip it to only see terminal & input.

== YET TODO ==

The first adaptation fixes the inflexible load store on every temp value in a let
production. I have the pseudo-code, but I need to confirm that I pull two values and
write an applyOperation() in compiler. Then I'll proceed to implement some of the
advanced features suggested afterward (strings, subroutines, for loop and arrays).

The subroutines are ambiguously defined. Deitel suggests defining them with gosub
(to initiate the jump) and return (to end the call). The trick involves whether that
means there is only one function per program, if it is Basiesque in the sense that
their gosub would specify a line number, or require a label to the start of the
description. I am heavily inclined to implement the former. I'm also a bit concerned
about shifting the return goto safely. Arguments & scope are harder still.

For loops are dead simple. I could add a while, but basic also used if-goto instead.

Inclined to add an index register, mainly for the packed string suggested, but also
for int arrays. (So it is only one access rather than two to get the value, because
this implementation is all about efficiency.) This would sound a total death knell
for the disassembler since the memory cells will hold two chars and the first is the
string's length.

Of course, if I compile to assembly rather than sml decimal, then there's no need for
a disassembler to xplain what the sml means. It will simply take care in flagging
the symbols and such in a clear manner. I'll branch when I do that, so as to not
muddy the standard version. If I decide to kludge an interpreter hybrid of the
compiler and simpletron, then that will also be on a different branch.

After that, the only thing remaining is to enliterate the program. I admit that
the literate programs wiki may not like it as it is outside of their canonical scope
but at least it will be here.