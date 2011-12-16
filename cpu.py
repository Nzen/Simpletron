
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
		# hur hur python, sure I can " -Cpu.word > self.acc > Cpu.word "
		# but short circuiting means it doesn't check both
	
	def fetch( self ): # vetted 11 12 7
		' get next, get indirected value '
		if self.mem.exceedAddrBound( self.pc ) :
			Cpu.coreDump( self, "Address out of range" )
		else :
			self.ir = self.mem.getFrom( self.pc )
			self.opCode = self.ir / Cpu.halfWord
			self.opAddr = self.ir % Cpu.halfWord
			if self.mem.exceedAddrBound( self.opAddr ) :
				coreDump( "Address out of range" )
			else:
				self.opVal = self.mem.getFrom( self.opAddr ) # separate low order; also, this is explicitly indirect addressing
				self.pc += 1
				# um, I hadn't been thinking to hard but I am putting the indirected value on top of opVal
				# I guess I should put it in a different register
				# dude, it's not a problem just think of it as another register
	
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
			if self.opVal == 0:
				Cpu.coreDump( self, "Divide by zero? No." )
			else:
				self.acc /= self.opVal
				Cpu.checkOverflow( self )
		# shit all these are getting the next instruction since fetch automatically puts it in there
		# two options: a) they indirect to the value of the intended address
		#					 b) these opCodes are direct: they test the address in the IR, not indirected
		# for the moment, I'll work with B.
		# in that case, the opAddr was already tested during the fetch, so there's no point in retesting
		elif Cpu.GOTO == self.opCode:
			print " going to %d" % self.opAddr
			self.pc = self.opAddr
		elif Cpu.GOTOZERO == self.opCode:
			print " going to %d if Acc is zero, it is %d" % ( self.opAddr, self.acc )
			if 0 == self.acc:
				self.pc = self.opAddr
		elif Cpu.GOTONEG == self.opCode:
			print " going to %d if Acc is neg, it is %d" % ( self.opAddr, self.acc )
			if 0 > self.acc:
				self.pc = self.opAddr
			'''
				if self.mem.exceedAddrBound( self.opVal ):
					Cpu.coreDump( self, "Address out of bounds " + str( self.opVal ) )
				else:
					self.pc = self.opVal
			elif Cpu.GOTOZERO == self.opCode:
				if 0 == self.acc:
					if self.mem.exceedAddrBound( self.opVal ):
						Cpu.coreDump( self, "Address out of bounds " + str( self.opVal ) )
					else:
						self.pc = self.opVal
			elif Cpu.GOTONEG == self.opCode:
				if 0 > acc:
					if self.mem.exceedAddrBound( self.opVal ):
						Cpu.coreDump( self, "Address out of bounds " + str( self.opVal ) )
					else:
						self.pc = self.opVal
			'''
		elif Cpu.LOAD == self.opCode:
			print " getting from %d" % ( self.opAddr )
			self.acc = self.mem.getFrom( self.opAddr )
			# damn it, I'm also going to make this one direct too, at least while the goto's are direct
		elif Cpu.STORE == self.opCode:
			print " saving %s at %d" % ( self.acc, self.opAddr ) # um why does the compiler think the Acc has a String?
			self.mem.setAt( self.opAddr, self.acc )
			# shit, more direct addressing. I may have to bite the bullet and indirect everything
			# I am loath because it is tedious while I am debugging everything
			# obviously, a compiler can handle itself either way though the wasted memory is ugly too
		else :
			Cpu.coreDump( self, "Unrecognized instruction" )	
			
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
		
		
		
		
		
		
		