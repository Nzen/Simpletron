
# postfix expression evaluator ; ie of the form 6 2 + 5 * 8 4 / -	[ assuming it started as (6 + 2) * 5 - 8 / 4 ]
# I'm going to assume that the postfix is a list, a string isn't worth the hassle

import stack
	
def __init__( self ) :
	self.operator = { "(": 0, "/": 1, "*": 2, "+": 3, "-": 4 }

def isOperator( opDict, candidate ) :
	return candidate in opDict
	
def evaluate( yVal, operator, xVal ) :
	if '+' is operator :
		return int( yVal ) + int( xVal )
	elif '-' is operator :
		return int( yVal ) - int( xVal )
	elif '*' is operator :
		return int( yVal ) * int( xVal )
	elif '/' is operator :
		return int( yVal ) / int( xVal )
	else :
		print "Unknown operator, undefined behavior mode activated"
		return yVal

def evaluatePostfix( postfix ) :
	' evaluates a postfix expression, I"m assuming the client sends a list of strings '
	operators = { "(": 0, "/": 1, "*": 2, "+": 3, "-": 4 } 
	tempVals = stack.Stack( )
	index = 0
	y = 0
	x = 0
	postfix.append( ">" ) # sentinel
	focus = postfix[ index ]
	while ">" != focus :
		if focus.isdigit( ) :
			tempVals.push( focus )
		elif isOperator( operators, focus ) :
			y = tempVals.pop( )
			x = tempVals.pop( )
			tempVals.push( evaluate( y, focus, x ) )
		else :
			print "I asked for a pure postfix expression. I just found a %s" % str( focus )
		index += 1
		focus = postfix[ index ]
	return tempVals.pop( )