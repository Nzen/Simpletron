
# testing postFixer and postFixEval
# ( 4 + 3 ) / 5 - 6 * 2 ==>> - / + 4 3 5 * 6 2

import postFixer
import postFixEval

test = "( 4 + 3 ) / 5 - 6 * 2"
print test
print "test should be 7/5-12, roughly 10.xx\n"

stepOne = postFixer.convertToPostFix( test, True ) # verbose mode
print postFixEval.evaluatePostfix( stepOne )