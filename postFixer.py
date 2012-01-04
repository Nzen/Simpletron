
# Nicholas Prado
# created 11 12 8

# convert & evaluate an infix equation as postfix:
# ( 4 + 3 ) / 5 - 6 * 2 ==>> - / + 4 3 5 * 6 2

import stack

def isOperator( opDict, candidate ) :
	return candidate in opDict
	
def higherPrecedence( opDic, focusOp, fromTempOp ) :
	if fromTempOp.isdigit( ) :
		return False
	x = opDic[ focusOp ]
	y = opDic[ fromTempOp ]
	return y >= x
	
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