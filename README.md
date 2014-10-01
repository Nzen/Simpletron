_This branch closed for the forseeable future. Reimplementing in Java is premature._

Deitel's _How to Program_ books (Java, C++, C#) have a couple exercises to emulate the other aspects of the programming environment. The first example is the VM that they call Simpletron. To incentivize learning Python, I implemented it. The second exercise involves creating a BASIC-esque compiler to generate its machine code. The complete version is tagged as '1.0' subsequent commits (& branches?) reflect optional improvements to the pair.

## RUNNING INSTRUCTIONS
(written for Python 2.6.7; Py 3.x need to alter prints and so on) 

To test cpu alone, uncomment comp needs lines 7 & 37 to read from the command line
and then use "comp.py [filename]".

To test the compiler use "testCompiler.py [filename]". It will ask whether you want
to run the file; any answer with y in it will run the .sml file through simpletron.
Simpletron is currently set to verbose in comp, flip it to only see terminal & input.

To test the postfixer (shuntyard/reverse polish expression), the instructions are
in testPost. It has an important warning within about input.

## SIMPLETRON ISA

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

xx is the address of the value to operate on. The math operations use the directed value on whatever is in the accumulator.

## SIMPLE COMPILER GRAMMER
(in Wirth's EBNF)

program = { statement };  
statement = line number, space , command expression, ( "\n"  { statement } );  
line number = number;  
number = digit, { digit };  
digit = "0" | "1" | "2" ; (*et cetera on integers x <= 9*)  
space = ? white space ?;  
command expression = unary expression | math expression | conditional expression;  
unary expression = ( unary command, ( identifier | number ) ) | ( "rem" , string ) ;  
unary command = "input" | "print" | "goto" ; (*actually goto can't jump to identifier value, yet*)  
math expression = "let", identifier , "=", ( identifier | number | equation );  
equation = ( parenthized equation | number | identifier ), { operator, equation } ;  
parenthized equation = "(", equation, ")" ;  
operator = "/" | "*" | "+" | "-" | "%" ;  
identifier = alphabetic character { alphabetic character } ; (*depends on how python interprets str.isdigit() else treated as id*)  
alphabetic character = "a" | "A" | "b" | "B" | "c" ; (*et cetera for english chars*)  
conditional expression = "if", identifier, relation, ( identifier | number ), "goto" , line number ;  
relation = ">" | "<" | "==" | ">=" | "<=" ; (*should add != or depreciated <>*)

This grammer was much more pleasant to write and is more accurate. I also left off the grammer implied by the extensions (for x; arrays). This is format is way more extensible than the Backhaus form I tried to use earlier.

### SIMPLE COMMANDS

* rem "" - commented string
* input x - value from terminal
* let x = ( 5 + 3 ) / 2 - assign via x = expression
* print 5 - print to terminal
* goto 6 - unconditional jump
* if 5 >= n goto 3 - conditional jump, form of if [ expression ] goto [ line number ]
* end - stop execution

### ADVANCED COMMANDS
for x = 10 to 50 step 10  
[statements]  
next ## signals end

def function ## definition  
[statements; no args, all vars global]  
return  
gosub function ## usage

* array tab = 5, 3, 6
* array tub[5]
* tab.len ## = 3
* tub[4] ## zero index, of course

## YET TODO

Gosub & return productions. Implementing scope and arguments is outside my current
interest.

For loops were more complicated than I thought. These and gosub really warrant a
pass to themselves for simplification, but I'll get by with a stack. These also
make me cringe at how monolithic this compiler is.

Inclined to add an index register to cpu, mainly for the packed string suggested,
but also for int arrays. (So it is only one access rather than two to get the
value. Obviously, this implementation is all about efficiency.) This would sound a
total death knell for the disassembler since the memory cells will hold two chars
and the first is the string's length.

On the assembler branch, that would no longer be a problem as the compiler would
purposefully emit Deitel's intermediate keywords (probably). I would also be able to
make the program more compact rather than sprawling out across the whole ram since
the data locations could be resolved by the assembler.

The interpreter branch feels less elegant, but is also in the pipeline. (Reading
about Basic & pascal has shown me interpreters have been a longstanding tool.)
Obviously, it would reject any forward references. Deitel wasn't clear whether
they expect it to be console or file based.

After that, the only thing remaining is to enliterate the program. I had only
planned to upload it to literateprogramming.org, but I accidentally created a
wiki for this project, so I guess it became the practice. The current version is
(largely) kosher for an enliteration. I was going to hem & haw about waiting to
implement the extensions, but the main value of the spec is in its canonical
aspect, not the extras that Deitel left ambiguous.

* more detail, use the wiki
