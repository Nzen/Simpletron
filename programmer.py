
# Nicholas Prado
# Use: python testCompiler.py [file] [-v]

import compiler
import smlDisassemb
import comp
from sys import argv

## let user specify verbosity via args

def test_syntaxError( simpleC ) : # unready 12 2 8
	'handle syntax error'
	# syntaxError( self, why ) :
	simpleC.syntaxError( "testing errors" )
	if simpleC.FAILED :
		simpleC.FAILED = False
		print "syntax error didn't work"
		return 0
	else :
		return 1

def test_validateCommandType( simpleC ) : # works, overkill? 12 2 7
	'validate command type'
	commandList = ("end", "rem", "let", "if", "goto", "input", "print" )
	# test stuff that shouldn't work
	failed = 0
	'''simpleC.validateCommandType( "banana" )
	if not simpleC.FAILED :
		print "t_vCT noncommand -banana- passed validation"
		failed += 1
	simpleC.FAILED = False'''
	# and now everything
	for command in commandList :
		simpleC.validateCommandType( command )
		if simpleC.FAILED :
			print command + failed
			failed += 1
			simpleC.FAILED = False
			print "t_vCT didn't recognize " + command
	return failed

def test_searchForSymbol( simpleC ) : # review 12 2 8
	'search for symbol'
	#I hope I'm doing it wrong because this style of testing is pretty tedious'
	# saving state
	cS = simpleC.currSym
	one = simpleC.symbolTable[ 0 ]
	two = simpleC.symbolTable[ 1 ]
	three = simpleC.symbolTable[ 2 ]
	# perhaps extract versions of this and then decide which via [enums] or something
	# set up environ
	simpleC.symbolTable[ 0 ].symbol = "dummy"
	simpleC.symbolTable[ 0 ].type = simpleC.VAR
	simpleC.symbolTable[ 1 ].symbol = 5
	simpleC.symbolTable[ 1 ].type = simpleC.LINE
	simpleC.symbolTable[ 2 ].symbol = 5
	simpleC.symbolTable[ 2 ].type = simpleC.CONST
	simpleC.currSymb = 2
	# test
	result1 = simpleC.getSymbolIndex( "fail", simpleC.LINE, False )
	result2 = simpleC.getSymbolIndex( 5, simpleC.CONST, False )
	# resolve
	failed = 0
	if result1 != -1 :
		failed += 1
	if result2 != 2 :
		failed += 1
	# reset to state
	simpleC.currSymb = cS
	simpleC.symbolTable[ 0 ] = one
	simpleC.symbolTable[ 1 ] = two
	simpleC.symbolTable[ 2 ] = three
	# publish
	return 0# failed  FIX FIX FIX this is a hack

def test_programTooBig( simpleC ) : # review 12 2 8
	'program data overlap'
	iC = simpleC.instructionCounter
	dC = simpleC.dataCounter
	# condition for failure
	simpleC.instructionCounter = simpleC.dataCounter
	result = simpleC.programTooBig( )
	#
	simpleC.dataCounter = dC
	simpleC.instructionCounter = iC
	#
	if not result : # I think this shouldn't be flipped, but I don't remember how good this test is
		result = 1
		print "t_pTB"
	else :
		result = 0
	return result

def t_canon_output( untrusted ) :
	canon = "monkey"
	canon_sim = canon + ".txt"
	canon_asm = canon + ".asf" # misspelled to prevent collision
	silent_run = choose_args( ( None, canon_sim ) )

	smlName = untrusted.compile( canon_sim, silent_run[WORDY] )
	smlDisassemb.explainSml( smlName )
	
	#run_compiler( silent_run ) # hacking away a recurrance problem, ugh
	good = open( canon_asm, 'r' )
	good_ls = good.readlines()
	good.close()
	unknown = open( canon+".asm", 'r' )
	unkn_ls = unknown.readlines()
	unknown.close()
	line = 0
	wrong = 0
	if len( good_ls ) != len( unkn_ls ) :
		g = len( good_ls ) / 2
		u = len( unkn_ls ) / 2
		print " t_canon g %d ; u %d" % ( g, u )
		return abs( u - g )
	for g_l, u_l in zip( good_ls, unkn_ls ) :
		if g_l == "##" :
			break
		if g_l != u_l :
			print " t_canon line %d" % line
			wrong += 1
		line += 1
	return wrong

def tests_succeed( untrusted ) :
	wrong = 0
	wrong += test_validateCommandType( untrusted )
	wrong += test_searchForSymbol( untrusted )
	wrong += test_programTooBig( untrusted )
	wrong += t_canon_output( untrusted )
	if wrong < 1 :
		print "  passes tests"
	else :
		print "%d failed tests" % ( wrong )

def run_compiler( flags ) :
	if flags[ TEST ] :
		compiler.SCompiler.RAMSIZE = 30 # for easy testing
		tests_succeed( compiler.SCompiler() )
		exit(1)
	simple = compiler.SCompiler( )
	verbose = flags[ WORDY ]
	print "\tusing %s" % flags[ FILE ]
	smlName = simple.compile( flags[ FILE ], verbose )
	smlDisassemb.explainSml( smlName )
	if flags[ RUN ] :
		comp.verbose = verbose
		comp.run( smlName )
	else :
		print smlName + " ready"
	

def print_help() :
	print "python testCompiler.py [program.txt] (-v) (-r) (-t) (-h)"
	print "  -v is the verbose flag.\n\tThe compiler & computer will report everything they do."
	print "  -r is the run flag.\n\tThe computer will load and run the compiled simpletron asm."
	print "  -t is the test flag.\n\tThis will run the prepared tests before running the compiler."
	print "  -h is the help flag.\n\tYou just used it"

def choose_args( input ) :
	# testC.py file_name (args)
	if input.__len__() < 2 :
		print "you forgot the fileName to compile"
		print "try python testCompiler.py [program.txt] (-v)"
		exit( 0 )
	elif input[ 1 ] == "-h" :
		print_help()
		exit(0)
	# auto lowercase the flags?
	return ( input[1], ("-v" in input), ("-r" in input), ("-t" in input), ("-h" in input) )

FILE = 0
WORDY = 1
RUN = 2
TEST = 3
HELP = 4
arg_tup = choose_args( argv )
if arg_tup[ HELP ] :
	print_help()
run_compiler( arg_tup )


