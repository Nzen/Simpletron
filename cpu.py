
# Nicholas Prado
# a virtual machine, initially adhering to Deitel's Simpletron spec

import ram

class Cpu( object ):

	word = 1000
	negWordLim = -1000
	halfWord = 100 # word / 10, so mod & divide separate hi/lo order correctly
	STOP = 0
	READ = 10
	WRITE = 11
	ADD = 20
	SUBTR = 21
	MULTP = 22
	DIVIDE = 23
	GOTO = 30
	GOTOZERO = 31
	GOTONEG = 32
	LOAD = 40
	STORE = 41
		
	def __init__( self, startPC, ramPtr, outputStatements ) :
		self.running = True
		self.pc = startPC # program counter
		self.acc = 0 # accumulator
		self.ir = 0 # instruction register
		self.opCode = 0 # instruction in the IR
		self.opAddr = 0 # address pointed to in IR
		self.opVal = 0 # value retrieved from opAddr
		self.mem = ramPtr
		self.verbose = outputStatements
		
	def checkOverflow( self ):
		' if exceeds wordsize, either positively or negatively '
		if Cpu.word < self.acc :
			Cpu.fail_coreDump( self, "Accumulator overflow" )
		elif Cpu.negWordLim > self.acc:
			Cpu.fail_coreDump( self, "Accumulator underflow" )
	
	def fetch( self ): # vetted 11 12 7
		' get next, get indirected value '
		if self.mem.exceedAddrBound( self.pc ) :
			Cpu.fail_coreDump( self, "Address out of range" )
		else :
			self.ir = self.mem.getFrom( self.pc )
			self.opCode = self.ir / Cpu.halfWord # separate high order
			self.opAddr = self.ir % Cpu.halfWord # separate low order
			if self.mem.exceedAddrBound( self.opAddr ) :
				fail_coreDump( "Address out of range" )
			else:
				self.opVal = self.mem.getFrom( self.opAddr )
				# this is a convenience, it may not be used if cpu writes to that location, or a goto
				self.pc += 1
	
	# each may be trivial, but extract for dict function magic
	def execute( self ):
		' elif field of the ISA '
		if Cpu.STOP == self.opCode:
			self.running = False
			if self.verbose :
				print "Halt program"
		elif Cpu.READ == self.opCode:
			if self.verbose :
				print " wait for terminal input"
			self.mem.setAt( self.opAddr, int( raw_input( " -- " ) ) )
		elif Cpu.WRITE == self.opCode: # to the terminal, am I assuming only ints here? perhaps separate int & char
			if self.verbose :
				print " print to terminal: ",
			print self.opVal
		elif Cpu.ADD == self.opCode:
			if self.verbose :
				print " add (acc) %s and %d" % ( self.acc, self.opVal )
			self.acc += self.opVal
			Cpu.checkOverflow( self )
		elif Cpu.SUBTR == self.opCode:
			if self.verbose :
				print " subtract (acc) %s and %d" % ( self.acc, self.opVal )
			self.acc -= self.opVal
			Cpu.checkOverflow( self )
		elif Cpu.MULTP == self.opCode:
			if self.verbose :
				print " multiply (acc) %s and %d" % ( self.acc, self.opVal )
			self.acc *= self.opVal
			Cpu.checkOverflow( self )
		elif Cpu.DIVIDE == self.opCode:
			if self.verbose :
				print " divide (acc) %s and %d" % ( self.acc, self.opVal )
			if 0 == self.opVal:
				Cpu.fail_coreDump( self, "Divide by zero? No." )
			else:
				self.acc /= self.opVal
				Cpu.checkOverflow( self )
		elif Cpu.GOTO == self.opCode:
			if self.verbose :
				print " naive goto ptr to %d" % self.opAddr
			Cpu.setPC( self, self.opAddr )
		elif Cpu.GOTOZERO == self.opCode:
			if self.verbose :
				print " if Acc (%d) is zero, goto %d" % ( self.acc, self.opAddr )
			if 0 == self.acc:
				Cpu.setPC( self, self.opAddr )
		elif Cpu.GOTONEG == self.opCode:
			if self.verbose :
				print " if Acc (%d) is neg, goto %d" % ( self.acc, self.opAddr )
			if 0 > self.acc:
				Cpu.setPC( self, self.opAddr )
		elif Cpu.LOAD == self.opCode:
			if self.verbose :
				print " load Acc with %d from %d" % ( self.opVal, self.opAddr )
			self.acc = self.opVal
		elif Cpu.STORE == self.opCode:
			if self.verbose :
				print " save acc, %s, into %d" % ( self.acc, self.opAddr )
			self.mem.setAt( self.opAddr, self.acc )
		else :
			Cpu.fail_coreDump( self, "Unrecognized instruction" )
			
	def run( self ):
		' fetch & execute while running '
		while self.running:
			Cpu.fetch( self )
			Cpu.execute( self )
			
	def setPC( self, addr ):
		' for the goto commands '
		if self.mem.exceedAddrBound( addr ) :
				fail_coreDump( "Address out of range" )
		else:
			self.pc = addr
	
	def fail_coreDump( self, reason ):
		' hardware error, so write the registers & memory '
		# I don't think this should silently fail, even if I don't want a verbose cpu
		print "core dump time: " + reason
		dump = open( "dump.txt", 'w' )
		dump.write( '\nVM fault: ' + reason + '\n' )
		dump.write( 'Program counter: ' + str( self.pc ) + '\t'  )
		dump.write( 'Instruction register: ' + str( self.ir ) + '\t'  )
		dump.write( 'Accumulator: ' + str( self.acc ) + '\n\n\n'  )
		self.mem.fail_coreDump( dump )
		dump.close( )
		self.running = False
		