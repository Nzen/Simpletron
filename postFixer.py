
# Nicholas Prado
# created 11 12 8

# convert & evaluate an infix equation as postfix:
# ( 6 + 2 ) * 5 - 8 / 4 ==>> 6 2 + 5 * 8 4 / -

# for some reason, above becomes 6 2 + 5 8 * + 4 + ; eval makes that to be 6

import stack

def isOperator( opDict, candidate ) :
	return candidate in opDict
	
def higherPrecedence( opDic, focusOp, fromTempOp ) :
	if fromTempOp.isdigit( ) :
		return False
	foc = opDic[ focusOp ]
	temp = opDic[ fromTempOp ]
	return temp >= foc # I think it is fouling because I numbered operators backwards and the stack doesn't delete?
	# flipping it empties the stack of the initial parenthesis
	
def convertSilently( infixString ) :
	' frozen until convertVerbosely works as expected, ie this does NOT work '
	operators = { "(": 0, ")": 1, "/": 2, "*": 3, "+": 4, "-": 5 } # so it wouldn't reInit every time
	# while my inclination is to find a python enum equivalent, the dict handles quietly
	temp = stack.Stack( )
	infix = infixString.split( ' ' )
	postFix = [ ]
	ind = 0
	next = 0
	temp.push( "(" )
	infix.append( ")" )
	char = ""
	bound = len( infix )
	
	while ( temp.notEmpty( ) and bound > ind ) :
	# Deitel's spec says the temp stack is enough, but I'm overflowing infix
	# for now, I'm going to nix that explicitly and recheck the algorithm later
		char = infix[ ind ]
		if char.isdigit( ) :
			postFix.append( char )
		elif "(" is char :
			temp.push( char )
		elif isOperator( operators, char ) :
			while higherPrecedence( operators, char, temp.peek( ) ) : # or maybe just do this once & continue?
				postFix.append ( temp.pop( ) )
			temp.push( char )
		elif ")" is char :
			while "(" != temp.peek( ) :
				postFix.append( temp.pop( ) )
		else :
			print "um, what is %s?" % char
		ind += 1
	
	return postFix

def convertVerbosely( infixString ) :
	' I didn"t want to muddy the other one with 1000 if statements '
	operators = { "(": 0, "/": 1, "*": 2, "+": 3, "-": 4 } # so it wouldn't reInit every time
	temp = stack.Stack( )
	infix = infixString.split( ' ' )
	postFix = [ ]
	ind = 0
	next = 0
	temp.push( "(" )
	infix.append( ")" )
	char = ""
	bound = len( infix )
	
	while ( temp.notEmpty( ) and bound > ind ) :
	# Deitel's spec says the temp stack is enough, but I'm overflowing infix
	# for now, I'm going to nix that explicitly and recheck the algorithm later
		char = infix[ ind ]
		print "char is %s" % char
		if char.isdigit( ) :
			print "  is digit"
			postFix.append( char )
		elif "(" is char :
			temp.push( char )
		elif isOperator( operators, char ) :
			print "  it's an operator"
			while higherPrecedence( operators, char, temp.peek( ) ) : # or maybe just do this once & continue?
				print "\tchar, %s is <= top of stack, %s" % ( char, temp.peek( ) )
				postFix.append ( temp.pop( ) )
			temp.push( char )
		elif ")" is char :
			print "time to search for the left parenthesis"
			while "(" != temp.peek( ) :
				print "\tfound %s, that's going onto postFix" % temp.peek( )
				postFix.append( temp.pop( ) )
		else :
			print "um, what is %s?" % char
		ind += 1
		print "ind is %d\n" % ind
		print "postfix : %s" % postFix
		temp.printStack( )
	return postFix

def convertToPostFix( infixString, verbose ) :
	postFix = []
	if verbose :
		postFix = convertVerbosely( infixString )
	else :
		postFix = convertSilently( infixString )
	return postFix


'''
Dijkstra's algorithm. Yeah, I thought theirs was a little underexplained
Read a token.
If the token is a number, then add it to the output queue.
If the token is a function token, then push it onto the stack.
If the token is a function argument separator (e.g., a comma):
	Until the token at the top of the stack is a left parenthesis, pop operators off the stack onto the output queue. If no left parentheses are encountered, either the separator was misplaced or parentheses were mismatched.
If the token is an operator, o1, then:
	while there is an operator token, o2, at the top of the stack, and
		either o1 is left-associative and its precedence is less than or equal to that of o2,
		or o1 is right-associative and its precedence is less than that of o2,
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