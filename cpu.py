
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
		self.opVal = 0 # operand from the IR
		self.mem = ramPtr
		
	def checkOverflow( self ):
		' if exceeds wordsize, pos or neg '
		if self.acc > Cpu.word or -Cpu.word > self.acc:
		# hur hur python, sure I can " -Cpu.word > self.acc > Cpu.word "
		# but short circuiting means it doesn't check both
			Cpu.coreDump( self, "Accumulator overflow" )
	
	def fetch( self ): # vetted 11 12 7
		' get next, get indirected value '
		if self.mem.exceedAddrBound( self.pc ) :
			coreDump( "Address out of range" )
		else :
			self.ir = self.mem.getFrom( self.pc )
			self.opCode = self.ir / Cpu.halfWord
			if self.mem.exceedAddrBound( self.ir % Cpu.halfWord ) :
				coreDump( "Address out of range" )
			else:
				self.opVal = self.mem.getFrom( self.ir % Cpu.halfWord ) # separate low order; also, this is explicitly indirect addressing
				self.pc += 1
				# um, I hadn't been thinking to hard but I am putting the indirected value on top of opVal
				# I guess I should put it in a different register
				
				# FIX THE ABOVE PROBLEM, I'm off to dinner
	
	def execute( self ):
		' elif field of the ISA '
		if Cpu.STOP == opCode:
			self.running = false
		elif Cpu.READ == opCode:
			self.acc = raw_input( " -- " )
		elif Cpu.WRITE == opCode: # to the terminal, am I assuming only ints here? perhaps separate int & char
			print self.acc
		elif Cpu.ADD == opCode:
			self.acc += opVal
			checkOverflow( )
		elif Cpu.SUBTR == opCode:
			self.acc -= opVal
			checkOverflow( )
		elif Cpu.MULTP == opCode:
			self.acc *= opVal
			checkOverflow( )
		elif Cpu.DIVIDE == opCode:
			if self.opVal == 0:
				coreDump( "Divide by zero? No." )
			else:
				self.acc /= opVal
				checkOverflow( )
		elif Cpu.GOTO == opCode:
			if self.mem.exceedAddrBound( self.opVal ):
				coreDump( "Address out of bounds" + str( self.opVal ) )
			else:
				self.pc = self.opVal
		elif Cpu.GOTOZERO == opCode:
			if 0 == self.acc:
				if self.mem.exceedAddrBound( opVal ):
					coreDump( "Address out of bounds" + str( self.opVal ) )
				else:
					pc = opVal
		elif Cpu.GOTONEG == opCode:
			if 0 > acc:
				if self.mem.exceedAddrBound( self.opVal ):
					coreDump( "Address out of bounds" + str( self.opVal ) )
				else:
					self.pc = self.opVal
		elif Cpu.LOAD == self.opCode:
			self.acc = self.mem.getFrom( self.opVal )
		elif Cpu.STORE == self.opCode:
			self.mem.setAt( self.opVal, self.acc )
		else :
			coreDump( "Unrecognized instruction" )	
			
	def run( self ):
		' fetch & execute while running '
		while running:
			fetch( )
			execute( )
			
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
		
		
		
		
		
		
		