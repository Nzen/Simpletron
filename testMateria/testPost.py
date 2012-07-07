
# testing postFixer and postFixEval
#( 6 + 2 ) * 5 - 8 / 4 ==>> 6 2 + 5 * 8 4 / - ==>> 38

import postFixer
import postFixEval

#test = "( 6 + 2 ) * 5 - 8 / 4"
test = "4 * ( 6 - 2 / 3 ) / 5 - 1"
#test = "( 4 + 5 ) * ( 2 - 5 )"
print test

stepOne = postFixer.convertToPostFix( test, False ) # verbose mode
print stepOne
#stepOne = [ '6', '2', '+', '5', '*', '8', '4', '/', '-' ]
#print postFixEval.evaluatePostfix( stepOne )