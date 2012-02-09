
# Nicholas Prado
# Might as well practice testing

import compiler
import smlPretty
import comp

def test_syntaxError( compiler ) : # unready 12 2 8
	'handle syntax error'
	# syntaxError( self, why ) :
	compiler.syntaxError( "testing errors" )

def test_validateCommandType( compiler ) : # works, overkill? 12 2 7
	'validate command type'
	endWorked = True
	remWorked = True
	letWorked = True
	ifWorked = True
	gotoWorked = True
	inputWorked = True
	printWorked = True
	bananaDidnt = True
	commandDict = {
		"end" : endWorked,
		"rem" : remWorked,
		"let" : letWorked,
		"if" : ifWorked,
		"goto" : gotoWorked,
		"input" : inputWorked,
		"print" : printWorked,
		}
	# test stuff that shouldn't work
	compiler.validateCommandType( "banana" )
	bananaDidnt = compiler.FAILED
	compiler.FAILED = False
	# and now everything
	for command in commandDict :
		compiler.validateCommandType( command )
		commandDict[ command ] = not compiler.FAILED # since I am asking if they worked
		compiler.FAILED = False
	return endWorked and remWorked and letWorked and ifWorked and gotoWorked and inputWorked and printWorked and bananaDidnt

def test_searchForSymbol( compiler ) : # review 12 2 8
	'search for symbol'
	#I hope I"m doing it wrong because this style of testing is pretty tedious'
	# saving state
	cS = compiler.currSym
	one = compiler.symbolTable[ 0 ]
	two = compiler.symbolTable[ 1 ]
	three = compiler.symbolTable[ 2 ]
	# perhaps extract versions of this and then decide which via [enums] or something
	
	# set up environ
	compiler.symbolTable[ 0 ].symbol = "dummy"
	compiler.symbolTable[ 0 ].type = tool.VAR
	compiler.symbolTable[ 1 ].symbol = 5
	compiler.symbolTable[ 1 ].type = tool.LINE
	compiler.symbolTable[ 2 ].symbol = 5
	compiler.symbolTable[ 2 ].type = tool.CONST
	compiler.currSymb = 2
	
	# test
	result1 = compiler.searchForSymbol( "fail", tool.LINE )
	result2 = compiler.searchForSymbol( 5, tool.CONST )
	
	# reset to state
	compiler.currSymb = cS
	compiler.symbolTable[ 0 ] = one
	compiler.symbolTable[ 1 ] = two
	compiler.symbolTable[ 2 ] = three
	
	# publish
	return result1 == -1 and result2 == 2
	'''
	symbolTable
	self.lineFlags
	self.smlData
	self.instructionCounter
	self.dataCounter
	self.currSym
	self.lastLine
	'''

def test_programTooBig( compiler ) : # review 12 2 8
	'program data overlap'
	iC = compiler.instructionCounter
	dC = compiler.dataCounter
	# condition for failure
	compiler.instructionCounter = compiler.dataCounter
	result = compiler.programTooBig( )
	#
	compiler.dataCounter = dC
	compiler.instructionCounter = iC
	return result

def test_reserveNewSymbol( compiler ) : # unready 12 2 8
	'reserve new symbol'
	return False

def test_comment( compiler ) : # unready 12 2 8
	'handle comment'
	return False

def test_finished( compiler ) : # unready 12 2 8
	'create halt instruction'
	return False

def test_userInput( compiler ) : # unready 12 2 8
	'create i/o wait flag'
	return False

def test_screenOutput( compiler ) : # unready 12 2 8
	'create printout'
	return False

def test_branch( compiler ) : # unready 12 2 8
	'create naive jump'
	return False

def test_conditional( compiler ) : # unready 12 2 8
	'create conditional jump'
	return False

def test_assignment( compiler ) : # unready 12 2 8
	'create assignment from expression'
	return False

tool = compiler.SCompiler( )

allFunctions = (
	test_reserveNewSymbol,
	test_comment,
	test_finished,
	test_userInput,
	test_screenOutput,
	test_branch,
	test_conditional,
	test_assignment,
	test_screenOutput,
	test_branch,
	test_programTooBig,
	test_searchForSymbol,
	test_validateCommandType,
	test_syntaxError
	)

compiler.SCompiler.RAMSIZE = 30
simple = compiler.SCompiler( )
file = "monkey.txt"
print "\tusing Deitel's %s" % file
#compiler.SCompiler.TESTING = True # well that's ugly; to change a class member in another module
smlName = simple.compile( file )
#print "validate worked? %r" % test_validateCommandType( simple )
# it was cute the first few times to pretty by hand. I'll CUT it when I issue the final version
smlPretty.prettify( smlName )
comp.run( smlName )
'''
# Oh yeah, that's what I'm talking about
for test in allFunctions :
	if not test( tool ) :
		print "\tNo ", 
		print test.__doc__ 
'''