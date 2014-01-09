
# Nicholas Prado
# because reading numerical SML codes isn't necessary

#from sys import argv
def explainSml( file ) :
	smlOps = {
		00 : "..", # halt or uninitialized data
		10 : "input to ",
		11 : "print from ",
		30 : "++ acc & from ",
		31 : "- - acc & from ",
		32 : "* * acc & from ",
		33 : "/ / acc & from ",
		20 : "load acc from ",
		21 : "store acc into ",
		40 : "naive goto ",
		41 : "if acc Negative goto ",
		42 : "if acc Zero goto ",
		43 : "stop execution "
		}
	#RAMSIZE = 100
	commentList = [ ]
	value = 0
	word = ""
	refList = [ ]
	reference = 0
	sml = open( file )
	for line in sml :
		if line == "##" :
			break
		value = int( line )
		word = smlOps[ value / 100 ]
		reference = value % 100
		commentList.append( word + str( reference ) + '\n' )
		#if ( reference > 0 or word > 0 ?) :
		#	refList.append( reference )
	sml.close( )
	#
	lineN = 0
	commentingBelow = open( file, 'a' )
	commentingBelow.write( "##\n" )
	for explanation in commentList :
		commentingBelow.write( str( lineN ) + ' ' + explanation )
		lineN += 1
		# trying to only output if the value is x > 0 or a reference, but that might cut a halt instruction
	commentingBelow.close( )