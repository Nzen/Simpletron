
Deitel's How to Program books (Java, C++, C#) have a couple exercises to emulate
the other aspects of the programming environment. The first example is the VM that
they call Simpletron. To incentivize learning Python, I am implemented it. The second
exercise involves creating a BASIC-esque compiler to generate its machine code. The
complete version is tagged as '1.0' subsequent commits (& branches?) reflect optional
improvements to the pair.

SIMPLETRON ISA:

Accumulator, IR, PC; RAM of 100 integers.

	READ = 10xx
	WRITE = 11xx
	LOAD = 20xx
	STORE = 21xx
	ADD = 30xx
	SUB = 31xx
	DIV = 32xx
	MUL = 33xx
	MOD = 34xx
	GOTO = 40xx
	GO_NEG = 41xx
	GO_ZERO = 42xx
	STOP = 43xx (also 0)

xx is the address of the value to operate on. Obviously, stop is unary. The math
operations use the directed value with whatever is in the accumulator.

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

It has been a long time, and rewriting this grammer has become tedious, but I think
that conforms. The point is that a line involves [line number] [command] [expression]
following the forms that the commands demand.

SIMPLE COMMANDS

rem - commented string
input - value from terminal
let - assign via x = expression
print - print to terminal
goto - unconditional jump
if - conditional jump, form of if [ expression ] goto [ line number ]
end - stop execution

RUNNING INSTRUCTIONS

(written for Python 2.6.7; Py 3.x need to alter prints and so on) 
To test cpu alone, uncomment comp needs lines 7 & 37 to read from the command line
and then use "comp.py [filename]".
To test the compiler use "testCompiler.py [filename]". It will ask whether you want
to run the file; any answer with y in it will run the .sml file through simpletron.
Simpletron is currently set to verbose in comp, flip it to only see terminal & input.

== YET TODO ==

Nearly finished with canonical specification for the simple compiler. It needs the
let production optimization and a little more refactoring in Cpu. I'll tag that commit
as 'canon' or 'full' and proceed to implement some of the advanced features suggested
at the end of the specification (strings, subroutines, for loop and arrays).

Deitel also suggests multivariable input/output as well as an interpreter. I'm not sure
how I would do that without a program hybridizing the interpreter & vm to ensure it
doesn't shut down once it tries to fetch a command that hasn't been interpreted yet.

After that, the only thing remains is to enliterate the program. I admit that
the literate programs wiki may not like it as it is outside of their canonical scope
but at least it will be here.

Also, I might put an intervening assembler between the simple compiler and simpletron.
SmlPretty is a human-oriented disassembler (in retrospect) and could easily be reversed
to produce the sml machine codes, given a suitable interface language. I'd put that on
a different branch, like the interpreter.