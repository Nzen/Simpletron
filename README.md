Deitel's _How to Program_ books (Java, C++, C#) have a couple exercises to emulate the other aspects of the programming environment. The first example is the VM that they call Simpletron. I implemented it to learn Python. The second exercise involves creating a BASIC-esque compiler to generate its machine code. The complete version is tagged as '1.0' subsequent commits & branches reflect optional improvements to the pair.

### RUNNING INSTRUCTIONS
(written for Python 2.6.7; Py 3.x need to alter prints and so on)

To test cpu alone, uncomment comp needs lines 7 & 37 to read from the command line
and then use "python comp.py [filename]".

To run the Simple compiler, use programmer. It expects either "python programmer.py [file] (flags)" or "python programmer.py -h". The latter will print the argument explanations. Possible options are *-v* verbose, *-r* load and run the asm, *-t* run tests, & *-h* print help.

comp.py represents the simpletron. Because I'm working on Simple currently, comp is a library rather than stand alone. To change that, uncomment line 7 (import args) & the line you want ~83. One can test it, run it with an asm file, or run the canonical Deitel version (ie feed it by hand).

To test the postfixer (shuntyard/reverse polish expression), the instructions are
in testPost. It has an important warning within about input.

### SIMPLETRON ISA

Accumulator, IR, PC; RAM of 100 integers. Advanced adds an index register.

	10xx = READ
	11xx = WRITE
	20xx = LOAD
	21xx = STORE
	30xx = ADD
	31xx = SUBTRACT
	32xx = DIVIDE
	33xx = MULTIPY
	34xx = MODULUS
	40xx = BRANCH
	41xx = BRANCHNEG
	42xx = BRANCHZERO
	43xx = HALT (also 0)

xx is the address of the value to operate on. The math operations use the directed value on whatever is in the accumulator.

### SIMPLE COMPILER GRAMMER
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
	identifier = alphabetic character { alphabetic character } ; (*via python str.isdigit() else, treated as id*)
	alphabetic character = "a" | "A" | "b" | "B" | "c" ; (*et cetera for english chars*)
	conditional expression = "if", identifier, relation, ( identifier | number ), "goto" , line number ;
	relation = ">" | "<" | "==" | ">=" | "<=" ; (*should add != or depreciated <> *)

This grammer was much more pleasant to write and is more accurate. I also left off the grammer implied by the extensions (for x; arrays). This is format is way more extensible than the Backhaus form I tried to use earlier.

### SIMPLE COMMANDS

* rem [text] - commented string
* input x - value from terminal
* let x = [expression] - assignment
* print # - print to terminal
* goto # - unconditional jump
* if [expression] goto # - conditional jump
* end - stop execution

### ADVANCED COMMANDS

	for x = 10 to 50 step 10  
	 [statements]  
	next

	# [statement]  
	 [statements]  
	return  
	gosub #

	array tab = 5, 3, 6
	array tub[5]
	tab.len
	tub[4]

## YET TODO

__Gosub__ & return productions. Implementing scope and arguments is outside my current
interest.

__For loops__ were more complicated than I thought. These and gosub really warrant a
pass to themselves for simplification, but I'll get by with a stack. These also
make me cringe at how monolithic this compiler is.

Inclined to add an __index register__ to cpu, mainly for the packed string suggested,
but also for int arrays. (So it is only one access rather than two to get the
value. Obviously, this implementation is all about efficiency.) This would sound a
total death knell for the disassembler since the memory cells will hold two chars
and the first is the string's length.

On the __assembler branch__, that would no longer be a problem as the compiler would
purposefully emit Deitel's intermediate keywords (probably). I would also be able to
make the program more compact rather than sprawling out across the whole ram since
the data locations could be resolved by the assembler.

The __interpreter branch__ feels less elegant, but is also in the pipeline. (Reading
about Basic & pascal has shown me interpreters have been a longstanding tool.)
Obviously, it would reject any forward references. Deitel wasn't clear whether
they expect it to be console or file based.

After that, the only thing remaining is to __enliterate the program__. I had only
planned to upload it to literateprogramming.org, but I accidentally created a
wiki for this project, so I guess it became the practice. The current version is
(largely) kosher for an enliteration. I was going to hem & haw about waiting to
implement the extensions, but the main value of the spec is in its canonical
aspect, not the extras that Deitel left ambiguous.

* more detail, use the wiki
