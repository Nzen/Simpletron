
# Nicholas Prado
# a virtual machine, largely adhering to Deitel's Simpletron spec

import ram

class Cpu( object ) :

	word = 1000
	halfWord = 100 # word / 10, so mod & divide separate hi/lo order correctly
	posWordLim = 9999
	negWordLim = -9999
	READ = 10
	WRITE = 11
	LOAD = 20
	STORE = 21
	ADD = 30
	SUBTRACT = 31
	DIVIDE = 32
	MULTIPLY = 33
	MODULUS = 34
	BRANCH = 40
	BRANCHNEG = 41
	BRANCHZERO = 42
	HALT = 43

	def __init__( self, startPC, ramPtr, outputDesirablility ) :
		self.running = True
		self.pc = startPC # program counter
		self.acc = 0 # accumulator
		self.ir = 0 # instruction register
		self.opCode = 0 # instruction in the IR
		self.opAddr = 0 # address pointed to in IR
		self.opVal = 0 # value retrieved from opAddr
		self.mem = ramPtr
		self.verbose = outputDesirablility # I think my earlier test with verbs was insufficient
		self.opVerbs = {
			0 : "Halt program",
			Cpu.HALT : "Halt program",
			Cpu.READ : " wait for terminal input",
			Cpu.WRITE : " print to terminal: ",
			Cpu.LOAD : " load Acc with " + str( self.opVal ) + " from " + str( self.opAddr ),
			Cpu.STORE : " save Acc (" + str( self.acc ) + ") into " + str( self.opAddr ),
			Cpu.ADD : " add (acc) " + str( self.acc ) + " and " + str( self.opVal ),
			Cpu.SUBTRACT : " subtract (acc) " + str( self.acc ) + " from " + str( self.opVal ),
			Cpu.MULTIPLY : " multiply (acc) " + str( self.acc ) + " and " + str( self.opVal ),
			Cpu.DIVIDE : " divide (acc) " + str( self.acc ) + " by " + str( self.opVal ),
			Cpu.MODULUS : " modulus (acc )" + str( self.acc ) + " by " + str( self.opVal ),
			Cpu.BRANCH : " naive goto ptr to " + str( self.opAddr ),
			Cpu.BRANCHZERO : " if Acc (%d) is zero, goto " + str( self.opAddr ),
			Cpu.BRANCHNEG : " if Acc (" + str( self.acc ) + ") is neg, goto " + str( self.opAddr )
			}
		
	def checkOverflow( self ):
		' if exceeds wordsize, either positively or negatively '
		if Cpu.posWordLim < self.acc :
			Cpu.fail_coreDump( self, "Accumulator overflow" )
		elif Cpu.negWordLim > self.acc:
			Cpu.fail_coreDump( self, "Accumulator underflow" )
	
	def fillRegisters( self ) :
		self.ir = self.mem.getFrom( self.pc )
		self.opCode = self.ir / Cpu.halfWord # separate high order
		self.opAddr = self.ir % Cpu.halfWord # separate low order
		if self.mem.exceedAddrBound( self.opAddr ) :
			Cpu.fail_coreDump( "Address " + str( self.opAddr ) + " out of range" )
		else:
			self.opVal = self.mem.getFrom( self.opAddr )
			# this is a convenience, it may not be used if cpu writes to that location, or a goto
			self.pc += 1
	
	def fetch( self ): # vetted 11 12 7
		' get next, get indirected value '
		if self.mem.exceedAddrBound( self.pc ) :
			Cpu.fail_coreDump( self, "Address " + str( self.pc ) + " out of range" )
		else :
			Cpu.fillRegisters( self )
	
	def halt( self ) :
		self.running = False
	
	def i_O( self, type, explanation ) :
		if self.verbose :
			print explanation,
		if type == Cpu.READ :
			self.mem.setAt( self.opAddr, int( raw_input( " -- " ) ) )
		else : # type == Cpu.WRITE
			print self.opVal
	''' advanced feature
	def strI_O( self, type, explanation ) : # PSEUDO: fix this copypasta
		# input; output to terminal; get length?
		if self.verbose :
			print explanation,
		if type == Cpu.READ :
			# raw input? file input? raw I think?
			# the trick is I only see what the loader put in so the compiler has to
			# generate the values and put them in smlData. This's compiler's job
			#hmm? self.opAddr -= 1
			for letter in explanation :
				self.mem.setAt( self.opAddr + 1, odr( letter ) - 27 )
		else : # type == Cpu.WRITE
			str = "" # get and interpret via chr( mem + 27 )
			print str'''
	
	def add( self ) :
		self.acc += self.opVal
		Cpu.checkOverflow( self )
	
	def subtr( self ) :
		self.acc -= self.opVal
		Cpu.checkOverflow( self )
	
	def multp( self ) :
		self.acc *= self.opVal
		Cpu.checkOverflow( self )
	
	def divid( self ) :
		if 0 == self.opVal:
			Cpu.fail_coreDump( self, "Divide by zero? No." )
		else:
			self.acc /= self.opVal
		Cpu.checkOverflow( self )
	
	def modul( self ) :
		# no need to check for overflow, the number will be smaller or same
		self.acc %= self.opVal

	def gotoNow( self ) :
		Cpu.setPC( self, self.opAddr )

	def gotoNeg( self ) :
		if 0 > self.acc :
			Cpu.setPC( self, self.opAddr )

	def gotoZer( self ) :
		if 0 == self.acc :
			Cpu.setPC( self, self.opAddr )
		
	def load( self ) :
		self.acc = self.opVal

	def save( self ) :
		self.mem.setAt( self.opAddr, self.acc )

	def execute( self ) :
		if self.opCode in Cpu.opSet :
			if self.opCode == Cpu.READ or self.opCode == Cpu.WRITE :
				Cpu.i_O( self, self.opCode, self.opVerbs[ self.opCode ] ) # different verbosity
				return
			if self.verbose :
				print self.opVerbs[ self.opCode ]
			execOp = Cpu.opSet[ self.opCode ]
			execOp( self ) # I can also skip this step by giving arguments above
		else :
			Cpu.fail_coreDump( self, "Unrecognized instruction" )

	def run( self ) :
		' fetch & execute while running '
		while self.running:
			Cpu.fetch( self )
			Cpu.execute( self )
			
	def setPC( self, addr ) :
		' for the goto commands '
		if self.mem.exceedAddrBound( addr ) :
				Cpu.fail_coreDump( "Address out of range" )
		else:
			self.pc = addr
	
	def fail_coreDump( self, reason ) :
		' hardware error, so write the registers & memory '
		# I don't think this should silently fail, even if I don't want a verbose cpu
		print "core dump time: " + reason
		dump = open( "dump.txt", 'w' )
		dump.write( '\nVM fault: ' + reason + '\n' )
		dump.write( 'Program counter: ' + str( self.pc ) + '\t'  )
		dump.write( 'Instruction register: ' + str( self.ir ) + '\t'  )
		dump.write( 'Accumulator: ' + str( self.acc ) + '\n\n\n'  )
		self.mem.coreDump( dump )
		dump.close( )
		self.running = False
	
	opSet = {
		0 : halt,
		HALT : halt,
		READ : i_O,
		WRITE : i_O,
		ADD : add,
		SUBTRACT : subtr,
		MULTIPLY : multp,
		DIVIDE : divid,
		MODULUS : modul,
		BRANCH : gotoNow,
		BRANCHZERO : gotoZer,
		BRANCHNEG : gotoNeg,
		LOAD : load,
		STORE : save
		}