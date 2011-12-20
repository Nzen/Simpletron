
# Nicholas Prado
# created 11 12 8

# convert & evaluate an infix equation as postfix:
# ( 4 + 3 ) / 5 - 6 * 2 ==>> - / + 4 3 5 * 6 2

import stack

def isOperator( candidate ) :
	pass
	# dictionary
	
def higherPrecedence( focus, fromTemp ) :
	pass
	# dictionary recalls operator vals, then I return the if
	#x = opDic[ focus ]
	#y = opDic[ fromTemp ]
	#return y >= x

def convertToPostFix( infix ) :
	' equation is a string expression of the form above '
	temp = stack.Stack( len( infix ) )
	# tokenize equation into a list
	ind = 0
	next = 0
	postFix = ""
	temp.push( "(" )
	infix.append( ")" )
	char = ""
	
	while ( temp.notEmpty( ) ) :
		# get next token from infix
		if isNumber( char ) : # isn't there a string function so I don't have to?
			postFix.append( str( char ) )
			next += 1 # do I still need this? not really, if append works
		elif "(" == char :
			temp.push( char )
		elif isOperator( char ) :
			while higherPrecedence( char, temp.peek( ) ) :
				postFix.append ( temp.pop( ) )
				# next += 1
			temp.push( char )
		elif ")" == char :
			while "(" not temp.peek( ) :
				postFix.append( temp.pop( ) )
				# next++
		else :
			pass
			# what else could it be?, increment char
	
	return postFix