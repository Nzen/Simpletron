
# Nicholas Prado
# a virtual machine, initially adhering to Deitel's Simpletron spec

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
verbose = True
#files = argv 
#files = files[ 1: ] # discards this script's name from the list of files
def run( files ) :
	ssd = ram.Ram( )
	cmd = cpu.Cpu( 0, ssd, verbose )
	ssd.loader( files )
	#testRam( ssd )
	#testCpu( ssd )
	cmd.run( )

'''
	Bad examples of using exec( ):

>>>
>>> for name in sys.argv[1:]:
>>>     exec "%s=1" % name
>>> def func(s, **kw):
>>>     for var, val in kw.items():
>>>         exec "s.%s=val" % var  # invalid!
>>> execfile("handler.py")
>>> handle()

	Good examples:

>>>
>>> d = {}
>>> for name in sys.argv[1:]:
>>>     d[name] = 1
>>> def func(s, **kw):
>>>     for var, val in kw.items():
>>>         setattr(s, var, val)
>>> d={}
>>> execfile("handle.py", d, d)
>>> handle = d['handle']
>>> handle()
'''
