
# Nicholas Prado
# a virtual machine, largely adhering to Deitel's Simpletron spec

import cpu
import ram
#from sys import argv # assuming you tell me which files you want loaded from HD

def testRam( usb ) :
	' unit test for ram module '
	print "Set addr 4 as -30\nPrint first five vals in reverse order\nDump ram to core.txt\n"
	for uu in range( 5, 0, -1 ) :
		print usb.getFrom( uu )
	core = open( "core.txt", 'w' )
	usb.coreDump( core )
	core.close( )

def testCpu( mem ) :
	cmd = cpu.Cpu( 0, mem )
	cmd.run( )
	# I wonder how I would test fetch and execute besides running?
	# I have indirectly tested them but getting the cpu's inernal state
	# isn't something I want to complicate with. Oh well it works anyway.
	core = open( "core.txt", 'w' )
	mem.coreDump( core )
	core.close( )

def invalid( input ) :
	bad_input = True
	word_lim = 9999
	lower_lim = -1 * word_lim
	try:
		val = int( input, 10 )
	except ValueError:
		return bad_input
	if val < lower_lim :
		return bad_input
	elif val > word_lim :
		return bad_input
	else :
		return not bad_input

def exit( input ) :
	return input == "##"

def deitel_version( ) :
	print '	*** Welcome to Simpletron! ***\n\
	*** Please enter your program one instruction  ***\n\
	*** (or data word) at a time into the input    ***\n\
	*** text field. I will display the location    ***\n\
	*** number and a question mark (?). You then   ***\n\
	*** type the word for that location. Enter the ***\n\
	*** hash twice to stop entering your program. ***'
	ssd = ram.Ram( )
	addr = 0
	while True :
		unknown = raw_input( str( addr ) + "_?_" )
		if exit( unknown ) :
			print "Stopping input. Running Simpletron ..."
			break
		elif invalid( unknown ) :
			print "\tinvalid, use {-9999 - 9999}"
			continue
		val = int( unknown )
		ssd.setAt( addr, val )
		addr += 1
	cmd = cpu.Cpu( 0, ssd, not verbose )
	cmd.run( )

def run( file ) :
	ssd = ram.Ram( )
	cmd = cpu.Cpu( 0, ssd, verbose )
	ssd.loader( file )
	#testRam( ssd )
	#testCpu( ssd )
	cmd.run( )

verbose = False # I've changed testCompiler to alter this
#run( argv[ 1 ] ) # uncomment here & line 7 to test cpu explicitly
#deitel_version()







