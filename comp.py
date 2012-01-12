
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
	core = open( "core.txt", 'w' )
	mem.coreDump( core )
	# so I can see RAM's contents even if CPU never halts or even succeeds silently
	core.close( )
	cmd = cpu.Cpu( 0, mem )
	cmd.run( )

files = argv 
files = files[ 1: ] # discards this script's name from the list of files

ssd = ram.Ram( )
cmd = cpu.Cpu( 0, ssd, True ) # true is for verbose mode

ssd.loader( files )
testRam( ssd )
#testCpu( ssd )
#cmd.run( )
