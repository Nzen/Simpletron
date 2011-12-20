
# postfix expression evaluator ; ie of the form 6 2 + 5 * 8 4 / -	[ assuming it started as (6 + 2) * 5 - 8 / 4 ]
# I'm going to assume that the postfix is a list, a string isn't worth the hassle

import stack

def isDigit( candidate ) :
	pass
	
def isOperator( candidate ) :
	pass
	# search a dict
	
def evaluate( yVal, operator, xVal ) :
	pass
	#elif field
	# return answer
	
def evaluatePostfix( postfix ) :
	' evaluates a postfix expression '
	tempVals = stack.Stack( len( postfix ) )
	index = 0
	y = 0
	x = 0
	postfix.append( ">" ) # sentinel
	focus = postfix[ index ]
	while ">" != focus :
		if isDigit( focus ) :
			tempVals.push( focus )
		elif isOperator( focus ) :
			y = tempVals.pop( )
			x = tempVals.pop( )
			tempVals.push( evaluate( y, focus, x ) )
		else
			print "I asked for a pure postfix expression. I just found a %s" % str( focus )
		index += 1
		focus = postfix[ index ]
	return tempVals.pop( )