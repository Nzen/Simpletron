
# Nicholas Prado
# a virtual machine, initially adhering to Deitel's Simpletron spec

 # may need to import ram or not, maybe ram should handle its loader
import ram

class Cpu( object ):

	word = 1000
	halfWord = 100 # half * 10, so mod & divide separate hi/lo order correctly
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
		
	def __init__( self, startPC, ramPtr ) :
		self.running = True
		self.pc = startPC # program counter
		self.acc = 0 # accumulator
		self.ir = 0 # instruction register
		self.opCode = 0 # instruction in the IR
		self.opAddr = 0 # address pointed to in IR
		self.opVal = 0 # value retrieved from opAddr
		self.mem = ramPtr
		
	def checkOverflow( self ):
		' if exceeds wordsize, pos or neg '
		if Cpu.word < self.acc :
			Cpu.coreDump( self, "Accumulator overflow" )
		elif -Cpu.word > self.acc:
			Cpu.coreDump( self, "Accumulator underflow" )
		self.running = False
	
	def fetch( self ): # vetted 11 12 7
		' get next, get indirected value '
		if self.mem.exceedAddrBound( self.pc ) :
			Cpu.coreDump( self, "Address out of range" )
			self.running = False
		else :
			self.ir = self.mem.getFrom( self.pc )
			self.opCode = self.ir / Cpu.halfWord # separate high order
			self.opAddr = self.ir % Cpu.halfWord # separate low order
			if self.mem.exceedAddrBound( self.opAddr ) :
				coreDump( "Address out of range" )
				self.running = False
			else:
				self.opVal = self.mem.getFrom( self.opAddr )
				self.pc += 1
	
	def validateIndirectAddr( self ) :
		' Repeating these checks 3 times is ugly '
		if self.mem.exceedAddrBound( self.opVal ):
			Cpu.coreDump( self, "Address out of bounds " + str( self.opVal ) )
			self.running = False
		else:
			return True
	
	def execute( self ):
		' elif field of the ISA '
		if Cpu.STOP == self.opCode:
			self.running = False
			print "Halt"
		elif Cpu.READ == self.opCode:
			self.acc = int( raw_input( " -- " ) )
			# doesn't need debug
		elif Cpu.WRITE == self.opCode: # to the terminal, am I assuming only ints here? perhaps separate int & char
			print self.acc	# or should I print the indirected value on the assumption that I already stored the Acc?
		elif Cpu.ADD == self.opCode:
			print " adding %s and %d" % ( self.acc, self.opVal )
			self.acc += self.opVal
			Cpu.checkOverflow( self )
		elif Cpu.SUBTR == self.opCode:
			print " minusing %s and %d" % ( self.acc, self.opVal )
			self.acc -= self.opVal
			Cpu.checkOverflow( self )
		elif Cpu.MULTP == self.opCode:
			print " timesing %s and %d" % ( self.acc, self.opVal )
			self.acc *= self.opVal
			Cpu.checkOverflow( self )
		elif Cpu.DIVIDE == self.opCode:
			print " ratioing %s and %d" % ( self.acc, self.opVal )
			if 0 == self.opVal:
				Cpu.coreDump( self, "Divide by zero? No." )
				self.running = False
			else:
				self.acc /= self.opVal
				Cpu.checkOverflow( self )
		# For ease in initial testing, these all did direct addressing. No longer.
		# A goto will point to the int value of the line number it actually intends to put in the PC
		# It may mean a bit more waste at ISA level, but that's what compilers are for.
		# However, the cpu won't check for bad values if the condition isn't met.
		elif Cpu.GOTO == self.opCode:
			print " going to %d" % self.opVal
			if Cpu.validateIndirectAddr( ) :
				self.pc = self.mem.getFrom( self.opVal )
		elif Cpu.GOTOZERO == self.opCode:
			print " ptr %d to %d if Acc is zero, it is %d" % ( self.opVal, self.mem.getFrom( self.opVal ), self.acc )
			if 0 == self.acc:
				if Cpu.validateIndirectAddr( self ) :
					self.pc = self.mem.getFrom( self.opVal )
		elif Cpu.GOTONEG == self.opCode:
			print " ptr %d to %d if Acc is neg, it is %d" % ( self.opVal, self.mem.getFrom( self.opVal ), self.acc )
			if 0 > self.acc:
				if Cpu.validateIndirectAddr( self ) :
					self.pc = self.mem.getFrom( self.opVal )
		elif Cpu.LOAD == self.opCode:
			print " getting from %d" % ( self.opVal )
			if Cpu.validateIndirectAddr( self ) :
				self.acc = self.mem.getFrom( self.opVal )
		elif Cpu.STORE == self.opCode:
			print " saving %s at %d" % ( self.acc, self.opVal )
			if Cpu.validateIndirectAddr( self ) :
				self.mem.setAt( self.opVal, self.acc )
		else :
			Cpu.coreDump( self, "Unrecognized instruction" )
			self.running = False
			
	def run( self ):
		' fetch & execute while running '
		while self.running:
			Cpu.fetch( self )
			Cpu.execute( self )
			
	def setPC( self, addr ):
		' just in case an SML OS has to set it low level rather than putting it in its own code? '
		self.pc = addr - 1
	
	def coreDump( self, reason ):
		' hardware error, so WRITE the registers & memory '
		print "core dump time: " + reason
		dump = open( "dump.txt", 'w' )
		dump.write( '\nVM fault: ' + reason + '\n' )
		dump.write( 'Program counter: ' + str( self.pc ) + '\t'  )
		dump.write( 'Instruction register: ' + str( self.ir ) + '\t'  )
		dump.write( 'Accumulator: ' + str( self.acc ) + '\n\n\n'  )
		self.mem.coreDump( dump )
		dump.close( )
		self.running = False
		
		
		
		
		
		
