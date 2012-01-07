
# testing postFixer and postFixEval
#( 6 + 2 ) * 5 - 8 / 4 ==>> 6 2 + 5 * 8 4 / - ==>> 38

import postFixer
import postFixEval

test = "( 6 + 2 ) * 5 - 8 / 4"
print test
print "test should be 38"

stepOne = postFixer.convertToPostFix( test, True ) # verbose mode
#stepOne = [ '6', '2', '+', '5', '*', '8', '4', '/', '-' ]
print postFixEval.evaluatePostfix( stepOne )