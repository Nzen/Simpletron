
# Nicholas Prado
# begun 12 1 11
# Compiler/assembler for Deitel's Simple language into SML for the Simpletron

from sys import argv
import postFixer
import symbolTableEntry

def writeSeparatedSmlData( failBlog, smlData, instructionLimit, valueLimit, ramSize ) :
	index = 0
	while index < instructionLimit :
		failBlog.write( smlData[ index ] )
		index += 1
	failBlog.write( " - data section" )
	index = valueLimit
	while index < ramSize :
		failBlog.write( smlData[ index ] )

def writeInterestingFlags( failBlog, lineFlags, ramSize ) :
	ind = 0
	while ind < ramSize :
		if lineFlags[ ind ] >= 0 :
			failBlog.write( ind + " " + lineFlags[ ind ] )
		ind += 1

def fail( symbolTable, lineFlags, smlData, instructionLimit, valueLimit, ramSize ) :
	failBlog = open( "compilerState.txt", 'w' )
	failBlog.write( "Finished instructions" )
	if valueLimit - instructionLimit > 10 :
		# if it's worth skipping the unwritten void in between instructions & data
		writeSeparatedSmlData( failBlog, smlData, smlData, instructionLimit, valueLimit, ramSize )
	else :
		for nn in smlData :
			failBlog.write( nn )
	failBlog.write( "Symbol Table" )
	for nn in symbolTable :
		failBlog.write( nn ) # I'll need to make that tostring equivalent
	failBlog.write( "flags set" )
	writeInterestingFlags( failBlog, lineFlags, ramSize )
	failBlog.close( )
	
def searchForSymbol( symbol, symbolTable, limit ) :
	ind = 0
	while ind <= limit :
		if symbolTable[ ind ].getSymbol == symbol :
			return ind
		ind += 1
	return -1

def comment( ) :
	symbolTable[ nextS ].setLocation( instructionCounter )
	nextS += 1
	
def finished( ) :
		sharedMem.setAt( instructionCounter, STOP )
		nextS += 1
		instructionCounter += 1

def userInput( ) :
		searchForSymbol( sym, symbolTable, nextSym )
		# set if unfound, ie -1
		# write to ram

def screenOutput( ) :
		searchForSymbol( sym, symbolTable, nextSym )
		# if unfound make anew
		# else, using found's location
		# ram set : write

def assignment( ) :
		# convert rest to postfix
		# eval postfix :
			# push mem locations
			# save commands rather than evaluating
			# save sub expression in location
			# store that answer
def branch( ) :
		# search symbolTable for the line number
		searchForSymbol( sym, symbolTable, nextSym )
		# found:
			# set ram with the goto at that location in the location of that symbol
		# else
			# flag[ instructionCounter ] = lineNumberSymbolReferenced
def conditional( ) :
		# verify the rest of the line
		# generate & save instructions for the conditional
		# search for ref line
		searchForSymbol( sym, symbolTable, nextSym )
		# store if found,
		# flag if not

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

commandList = {
	"end" : finished,
	"remark" : comment,
	"let" : assignment,
	"if" : conditional,
	"goto" : branch,
	"input" : userInput,
	"print" : screenOutput,
	}
symbolTable = [ symbolTableEntry.TableEntry( ) ] * RAMSIZE
# I may would make this a dict if it didn't also have 2 vars per name. Research is in order.
lineFlags[ -1 ] * RAMSIZE
smlData = [ 0 ] * RAMSIZE
instructionCounter = 0
dataCounter = RAMSIZE
nextS = 0 # next Symbol table entry in the list

# ask or get from the arguments, only one at a time for the moment
fileName = argv[ 1 ]
simpleProgram = open( fileName )
# FIRST PASS
for line in simpleProgram :
	segment = line.split( ' ' )
	''' check if this line number is greater than last, else syntax error '''
	# store the line number
	symbolTable[ nextS ].setType( LINE )
	symbolTable[ nextS ].setSymbol( segment[ 0 ] ) # in this case, the line number
	comm = segment[ 1 ]
	if comm not in commandList :
		print "unrecognized command at %s" % symbolTable[ nextS ].getSymbol( )
		continue
	else :
		newInstruc = commandList[ comm ]
		newInstruc( ) # providing it with anything it may need
		
		instructionCounter += 1 # wait one second. That might foul the first instruction FIX?
		symbolTable[ nextS ].setLocation( instructionCounter )
		nextS += 1
