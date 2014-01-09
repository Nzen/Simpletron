
# testing postFixer and postFixEval
#( 6 + 2 ) * 5 - 8 / 4 ==>> 6 2 + 5 * 8 4 / - ==>> 38
# to test, uncomment lines 8, 11-13, 23, 24
	# be aware, convert silent operates on lists, verbose converts a string
	# so evaluate the appropriate conversion

import postFixer
import postFixEval
#from sys import argv

verbose = False
#if argv.__len__() > 1 :
#	if argv[ 1 ] == '-v' :
#		verbose = True
yes = '0'
while yes == '0' :
	test = raw_input( "  expression to fix -- " )
	print test # .rstrip( '\n' )
	stepOne = postFixer.convertToPostFix( test, verbose ) # verbose mode
	yes = raw_input( "\tagain? (1/0) -- " )


# stepOne = [ '6', '2', '+', '5', '*', '8', '4', '/', '-' ] # expression from header
# stepOne = [ '12', '10', '-', '4', '+', '2', '-' ]
# print postFixEval.evaluatePostfix( stepOne )