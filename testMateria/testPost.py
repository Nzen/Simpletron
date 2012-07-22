
# testing postFixer and postFixEval
#( 6 + 2 ) * 5 - 8 / 4 ==>> 6 2 + 5 * 8 4 / - ==>> 38

import postFixer
#import postFixEval

#test = "( 6 + 2 ) * 5 - 8 / 4"
#test = "4 * ( 6 - 2 / 3 ) / 5 - 1"
#test = "( 4 + 5 ) * ( 2 - 5 )"
yes = 0
while True :
	yes = raw_input( "\tagain? (1/0) -- " )
	if yes == '0' :
		break
	else :
		test = raw_input( "  expression to fix -- " )
		print test # .rstrip( '\n' )
		stepOne = postFixer.convertToPostFix( test, True ) # verbose mode
		print stepOne
#stepOne = [ '6', '2', '+', '5', '*', '8', '4', '/', '-' ]
#print postFixEval.evaluatePostfix( stepOne )