
# Nicholas Prado
# a virtual machine, initially adhering to Deitel's Simpletron spec

import cpu
import ram
from sys import argv # assuming you tell me which files you want loaded from HD

"""
Three classes:
	Comp(uter) that is main and loads the program(s),
	CPU that is a Von Neumann, accumulator Risc
	Ram, a wrapper for a list
"""

def testRam( usb ) :
	' unit test for ram module, setting tested in the loader below '
	for uu in range( 5, 0, -1 ) :
		print usb.getFrom( uu )
	core = open( "core.txt", 'w' )
	usb.coreDump( core )
	core.close( )

def testCpu( mem ) :
	core = open( "core.txt", 'w' )
	mem.coreDump( core )
	# so I can see RAM's contents even if CPU never halts or even succeeds silently
	core.close( )
	cmd = cpu.Cpu( 0, mem )
	cmd.run( )

files = argv 

ssd = ram.Ram( )
cmd = cpu.Cpu( 0, ssd, True ) # true is for verbose mode

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
	#testCpu( ssd )
	cmd.run( )
finally: # is there a catch instead?
	#print "filo exception probably"
	pass
