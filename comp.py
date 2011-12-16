
# Nicholas Prado
# a virtual machine, initially adhering to Deitel's Simpletron spec

import cpu
import ram
from sys import argv # assuming you tell me which files you want loaded from HD

def testRam( usb ) :
	' unit test for ram module, setting tested in the loader below '
	for uu in range( 5, 0, -1 ) :
		print usb.getFrom( uu )
	core = open( "core.txt", 'w' )
	usb.coreDump( core )
	core.close( )

def testCpu( mem ) :
	cmd = cpu.Cpu( 0, mem )
	cmd.run( )
	
"""
Three classes:
	Comp(uter) that is main and loads the program(s),
	CPU that is a Von Neumann, accumulator Risc
	Ram, a wrapper for a list
"""
files = argv # I am a list?

ssd = ram.Ram( )
#cmd = cpu.Cpu( 0, ssd )

# fill RAM with data & machine code
memNext = 0
temp = 0
files = files[ 1: ] # discards this script's name from the list of files
try:
	# Loader
	for nn in files :
		hdSector = open( nn )
		for line in hdSector:
			#print "%d %s" % ( temp, line ), # cut after debugging
			if not line.startswith( "##" ) :
				if ssd.exceedAddrBound( memNext ) :
					continue
				else :
					ssd.setAt( memNext, int( line[ :-1 ] ) )
					memNext += 1
			else:
				break # so I can put comments below
			temp += 1
		hdSector.close( )
	#testRam( ssd )
	testCpu( ssd )
	#cmd.run( )
finally:
	#print "filo exception probably"
	pass
