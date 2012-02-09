
# Nicholas Prado
# because reading numerical SML codes isn't necessary

#from sys import argv
def prettify( file ) :
	smlOps = {
		00 : "..", # halt or uninitialized data
		10 : "input to ",
		11 : "print from ",
		20 : "++ acc & from ",
		21 : "- - acc & from ",
		22 : "* * acc & from ",
		23 : "/ / acc & from ",
		30 : "goto ",
		31 : "if acc Negative goto ",
		32 : "if acc Zero goto ",
		40 : "load acc from ",
		41 : "store acc into " }
	#RAMSIZE = 100
	commentList = [ ]
	value = 0
	word = ""
	#file = argv[ 1 ] # can be modified for multiple, but why bother?
	sml = open( file )
	for line in sml :
		if line == "##" : #\n # ie, I've run this before. oh. but then it'll append past the first commenting. hmm think about that
			break
		value = int( line )
		word = smlOps[ value / 100 ]
		commentList.append( word + str( value % 100 ) + '\n' )
	sml.close( )
	#
	lineN = 0
	commentingBelow = open( file, 'a' )
	commentingBelow.write( "##\n" )
	for explanation in commentList :
		commentingBelow.write( str( lineN ) + ' ' + explanation )
		lineN += 1
	commentingBelow.close
