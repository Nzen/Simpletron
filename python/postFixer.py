
# Nicholas Prado
# created 11 12 8

# convert & evaluate an infix equation as postfix:
# ( 6 + 2 ) * 5 - 8 / 4 ==>> 6 2 + 5 * 8 4 / -

import stack

def isOperator( opDict, candidate ) :
	return candidate in opDict
	
def higherPrecedence( opDic, focusOp, fromTempOp ) :
	focus = opDic[ focusOp ]
	stored = opDic[ fromTempOp ]
	if "(" == stored :
		return False
	else :
		return focus <= stored
	
def convertSilently( infix ) :
	' no outputs of operations '
	operators = { "(": 0, "/": 3, "*": 3, "+": 2, "-": 2, "%" : 4 }
	opStack = stack.Stack( )
	#infix = infixString.split( ' ' ) # comment for compiller # uncomment for deliberate testing, rename arg
	postFix = [ ]
	ind = 0
	next = 0
	opStack.push( "(" )
	infix.append( ")" )
	char = ""
	bound = len( infix )
	
	while ( bound > ind ) :
		char = infix[ ind ]
		if char.isdigit( ) :
			postFix.append( char )
		elif char.isalpha( ) :
			postFix.append( char )
		elif "(" is char :
			opStack.push( char )
		elif isOperator( operators, char ) :
			while higherPrecedence( operators, char, opStack.peek( ) ) : # or maybe just do this once & continue?
				postFix.append ( opStack.pop( ) )
			opStack.push( char )
		elif ")" is char :
			while opStack.peek( ) is not "(":
				postFix.append( opStack.pop( ) )
		else :
			print "um, what is %s?" % char
		ind += 1
	while opStack.notEmpty( ) :
		if opStack.peek( ) is not "(" :
			postFix.append( opStack.pop( ) )
		else :
			opStack.pop( )
	
	return postFix

def convertVerbosely( infixString ) :
	' blow by blow. also this operates on a string, not a list like silently does '
	operators = { "(": 0, "/": 3, "*": 3, "+": 2, "-": 2, "%" : 4 }
	opStack = stack.Stack( )
	infix = infixString.split( ' ' )
	postFix = [ ]
	ind = 0
	next = 0
	opStack.push( "(" )
	infix.append( ")" )
	char = ""
	bound = len( infix )
	
	while ( bound > ind ) :
		char = infix[ ind ]
		print "char is %s " % char,
		if char.isdigit( ) :
			print "  is digit"
			postFix.append( char )
		elif char.isalpha( ) :
			postFix.append( char )
		elif "(" is char :
			opStack.push( char )
		elif isOperator( operators, char ) :
			print "  it's an operator"
			if opStack.notEmpty( ) :
				while opStack.notEmpty( ) and higherPrecedence( operators, char, opStack.peek( ) ) :
					#print "\tchar, %s is <= top of stack, %s" % ( char, opStack.peek( ) )
					postFix.append ( opStack.pop( ) )
			opStack.push( char )
		elif ")" is char :
			print "time to search for the left parenthesis"
			while "(" != opStack.peek( ) :
				print "\tfound %s, that's going onto postFix" % opStack.peek( )
				postFix.append( opStack.pop( ) )
			# discard ( ?
		else :
			print "um, what is %s?" % char
		ind += 1
		#print "ind is %d\n" % ind
	while opStack.notEmpty( ) :
		if opStack.peek( ) is not "(" :
			postFix.append ( opStack.pop( ) )
		else :
			opStack.pop( )
	print "postfix : %s" % postFix # I assume only wanting to see the final result
	return postFix

def convertToPostFix( infixString, verbose ) :
	if verbose :
		return convertVerbosely( infixString )
	else :
		return convertSilently( infixString )

'''
	Dijkstra's algorithm. Yeah, I thought theirs was a little underexplained
Read a token.
If the token is a number, then add it to the output queue.
If the token is a function token, then push it onto the stack.
If the token is a function argument separator (e.g., a comma):
	Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue. If no left parentheses are encountered, either the separator was misplaced or parentheses were mismatched.
If the token is an operator, o1, then:
	while there is an operator token, o2, at the top of the stack, and o1's precedence is less than or equal to that of o2
		pop o2 off the stack, onto the output queue;
	push o1 onto the stack.
If the token is a left parenthesis, then push it onto the stack.
If the token is a right parenthesis:
	Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue.
	Pop the left parenthesis from the stack, but not onto the output queue.
	If the token at the top of the stack is a function token, pop it onto the output queue.
	If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.
When there are no more tokens to read:
	While there are still operator tokens in the stack:
	If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses.
	Pop the operator onto the output queue.
Exit.
'''