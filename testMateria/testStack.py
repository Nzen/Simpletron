
import stack

print "this is what I get for implementing a stack, now I have to test it"
stuff = [ 1, 2, 3, 4, 5, 6 ]
hole = stack.Stack( )

inp = ""
dex = 0
lim = len( stuff )
while inp != "1" :
	if "o" == inp :
		print "\tpushing %d" % stuff[ dex ]
		hole.push( stuff[ dex ] )
		dex += 1
	elif "t" == inp :
		print "\tpopping ",
		print hole.pop( )
	hole.printStack( )
	if dex >= lim :
		dex = 0
	inp = raw_input( "o to push; t to pop; 1 to stop -- " )