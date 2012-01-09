
# postfix expression evaluator ; ie of the form 6 2 + 5 * 8 4 / - , which evaluates to 38
# I'm going to assume that the postfix is a list, a string isn't worth the hassle

import stack

def isOperator( opList, candidate ) :
	return candidate in opList
	
def evaluate( yVal, operator, xVal ) :
	if '+' is operator :
		#print "%d + %d = %d" % ( int( yVal ), int( xVal ), int( yVal ) + int( xVal ) )
		return int( yVal ) + int( xVal )
	elif '-' is operator :
		#print "%d - %d = %d" % ( int( yVal ), int( xVal ), int( yVal ) - int( xVal ) )
		return int( yVal ) - int( xVal )
	elif '*' is operator :
		#print "%d * %d = %d" % ( int( yVal ), int( xVal ), int( yVal ) * int( xVal ) )
		return int( yVal ) * int( xVal )
	elif '/' is operator :
		#print "%d / %d = %d" % ( int( yVal ), int( xVal ), int( yVal ) / float( xVal ) )
		return int( yVal ) / float( xVal )
	else :
		print "  Unknown operator, undefined behavior mode activated"
		return yVal

def evaluatePostfix( postfix ) :
	' evaluates a postfix expression, I"m assuming the client sends a list of strings '
	#print "\tevaluate post %s" % postfix
	operators = [ "/", "*", "+", "-" ]
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
			x = tempVals.pop( )
			y = tempVals.pop( )
			tempVals.push( evaluate( y, focus, x ) )
			tempVals.printStack( )
		else :
			print "I asked for a pure postfix expression. I just found a %s" % focus
		index += 1
		focus = postfix[ index ]
	return tempVals.pop( )