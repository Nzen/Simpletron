
# Nicholas Prado
# begun 12 1 11
# Compiler/assembler for Deitel's Simple language into SML for the Simpletron

import ram
import postFixer
import symbolTableEntry

STOP = 0000
READ = 1000
WRITE = 1100
ADD = 2000
SUBTR = 2100
MULTP = 2200
DIVIDE = 2300
GOTO = 3000
GOTOZERO = 3100
GOTONEG = 3200
LOAD = 4000
STORE = 4100
RAMSIZE = 100
LINE = 0
VAR = 1
CONST = 2

symbolTable = [ symbolTableEntry.TableEntry( ) ] * RAMSIZE
lineFlags[ -1 ] * RAMSIZE
instructionCounter = 0
dataCounter = RAMSIZE
sharedMem = ram.Ram( )
nextS = 0 # next Symbol table entry in the list

# ask or get from the arguments
openFile( fileName )
while not EOF :
	line = readline( )
	segment = line.split( ' ' )
	## check if this line number is greater than last, else syntax? error
	# store the line number
	symbolTable[ nextS ].setType( LINE )
	symbolTable[ nextS ].setSymbol( segment[ 0 ] ) # in this case, the line number
	# handle REMARK
	command = segment[ 1 ]
	if "remark" == command :
		symbolTable[ nextS ].setLocation( instructionCounter )
		nextS += 1
		continue
	else :
		instructionCounter += 1
		symbolTable[ nextS ].setLocation( instructionCounter )
		nextS += 1
		# handleCommand( command, segment[ 2: ], everythingElse )
		# I'm not sure whether I want to make it here or in a function.
		# function is better but I have to pass it a bunch of stuff. hmm
		# should I be using a dict to reference the functions instead?
		# form of simpleCommands[ command ]
		if "end" == command :
			sharedMem.setAt( instructionCounter, STOP )
			nextS += 1
			instructionCounter += 1
			continue
		elif "input" == command :
			# search for symbol
			# set if unfound
			# write to ram
		elif "print" == command :
			# search for symbol
			# if unfound make anew
			# else, using found's location
			# ram set : write
		elif "let" == command :
			# convert rest to postfix
			# eval postfix :
				# push mem locations
				# save commands rather than evaluating
				# save sub expression in location
				# store that answer
		elif "goto" == command :
			# search symbolTable for the line number
			# found:
				# set ram with the goto at that location in the location of that symbol
			# else
				# flag[ instructionCounter ] = lineNumberSymbolReferenced
		elif "if" == command :
			# verify the rest of the line
			# generate & save instructions for the conditional
			# search for ref line
			# store if found,
			# flag if not
		else :
			print "unrecognized command at %s" % symbolTable[ nextS - 1 ].getSymbol( )