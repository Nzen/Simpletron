
# Nicholas Prado
# begun 12 1 11
# Compiler/assembler for Deitel's Simple language into SML for the Simpletron

import postFixer
# import symbolTableEntry

class TableEntry( object ) : # tentative 12 1 23
	'simple record for each element of the simple values'
	def __init__( self ) :
		symbol = ""
		type = 0 # line var or constVal
		location = 0

class SCompiler( object ) :

	SCompiler.STOP = 0000
	SCompiler.READ = 1000
	SCompiler.WRITE = 1100
	SCompiler.ADD = 2000
	SCompiler.SUBTR = 2100
	SCompiler.MULTP = 2200
	SCompiler.DIVIDE = 2300
	SCompiler.GOTO = 3000
	SCompiler.GOTOZERO = 3100
	SCompiler.GOTONEG = 3200
	SCompiler.LOAD = 4000
	SCompiler.STORE = 4100
	SCompiler.RAMSIZE = 100
	SCompiler.LINE = 0
	SCompiler.VAR = 1
	SCompiler.CONST = 2
	
	def __init__( self ) : # tentative 12 1 23
		self.commandList = {
			"end" : finished,
			"remark" : comment,
			"let" : assignment,
			"if" : conditional,
			"goto" : branch,
			"input" : userInput,
			"print" : screenOutput,
			}
		self.symbolTable = [ TableEntry( ) ] * SCompiler.RAMSIZE
		self.lineFlags[ -1 ] * SCompiler.RAMSIZE
		self.smlData = [ 0 ] * SCompiler.RAMSIZE
		self.instructionCounter = -1
		self.dataCounter = SCompiler.RAMSIZE
		self.currSym = -1
		
	def syntaxError( self, why ) : # unreliable yet tentative 12 1 23
		# consider tracking the actual line number rather than client supplied
		print "%s at %s" % ( why, self.symbolTable[ currSym ].symbol ) # unless it is the first line number
		exit( 1 )

	def searchForSymbol( self, sought ) : # tentative 12 1 23
		'returns index of symbol or -1 if not present'
		ind = 0
		limit = self.currSym
		while ind <= limit :
			if self.symbolTable[ ind ].symbol == sought :
				return ind
			ind += 1
		return -1

	def programTooBig( self ) : # tentative 12 1 23
		'instructions build down, data builds up. should the twain meet, Ram is full'
		return self.instructionCounter >= self.dataCounter
	
	def reserveNewSymbol( self, symb, theType ) : # unreliable yet tentative 12 1 23
		'I don"t trust this version even conceptually yet as it reflects screenOut"s initial needs'
		# so it may not be general enough yet
		self.currSym += 1
		self.symbolTable[ currSym ].type = theType
		self.symbolTable[ currSym ].symbol = symb
		self.dataCounter -= 1
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many variables reserved: " + symb )
		self.symbolTable[ currSym ].location = self.dataCounter
		if theType == SCompiler.CONST :
			self.smlData[ dataCounter ] = int( self.symbolTable[ currSym ].symbol )
			
	def comment( self, restOfLine ) : # tentative 12 1 23
		"# remark lorem ipsum dolores set amet"
		self.instructionCounter -= 1
		# remarks don't generate instructions, hence reset
		if self.instructionCounter >= 0 :
			self.symbolTable[ self.currSym ].location = self.instructionCounter
		else :
			self.symbolTable[ self.currSym ].location = 0
		# but the first time IC is -1 rather than 0, so leaving it thus would underflow
		# if a goto pointed at it. I'd like to optimize this into a single check but not now.
		pass # this & similars are because notepad++ doesn't fold the comments below a function
		
	def finished( self, restOfLine ) : # tentative 12 1 23
		"# halt"
		self.smlData[ instructionCounter ] = SCompiler.STOP

	def userInput( self, restOfLine ) : # tentative 12 1 23
		"# input x, meaning, store input in var x"
		if restOfLine[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "can not use constants as variable names" )
		where = SCompiler.searchForSymbol( self, sym )
		if where < 0 :
			SCompiler.reserveNewSymbol( self, restOfLine[ 0 ], SCompiler.VAR )
			self.smlData[ instructionCounter ] = SCompiler.READ + dataCounter
		else :
			self.smlData[ instructionCounter ] = SCompiler.READ + self.symbolTable[ where ].location
			# if unfound make anew
			# else, using found's location
			# ram set : SCompiler.READ from keyboard
		pass

	def screenOutput( self, restOfLine ) : # tentative 12 1 23
		"# print x" # also, print a #, however all variables are initialized to 0 so be wary
		where = SCompiler.searchForSymbol( self, restOfLine[ 0 ] )
		if where < 0 :
			# unfound: reserve space
			type = 0
			if restOfLine.isdigit( ) :
				type = SCompiler.CONST
			else :
				type = SCompiler.VAR
			SCompiler.reserveNewSymbol( self, restOfLine[ 0 ], type )
			self.smlData[ instructionCounter ] = SCompiler.WRITE + dataCounter # self.symbolTable[ currSym ].location
		else :
			# I found it, so write onscreen
			self.smlData[ instructionCounter ] = SCompiler.WRITE + self.symbolTable[ where ].location
			
			'''self.currSym += 1
			self.symbolTable[ currSym ].symbol = restOfLine[ 0 ]
			self.dataCounter -= 1
			if SCompiler.programTooBig( self ) :
				SCompiler.syntaxError( self, "Too many variables reserved: " + restOfLine )
			self.symbolTable[ currSym ].location = self.dataCounter'''
		pass
				
	def branch( self, restOfLine ) : # WORKING HERE 12 1 23
		"# goto #2"
		if not restOfLine[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "can not jump to variable value line, only constants" )
		# search symbolTable for the referenced line number
		where = SCompiler.searchForSymbol( self, restOfLine[ 0 ] )
		# found:
			# set ram with the goto at that location in the location of that symbol, REPHRASE
		if where >= 0 :
			self.smlData[ self.instructionCounter ] = SCompiler.GOTO + self.symbolTable[ where ].location
		else :
			# flag for later substitution
			self.lineFlags[ self.instructionCounter ] = int( restOfLine[ 0 ] )
			self.smlData[ self.instructionCounter ] = SCompiler.GOTO
		pass
				
	def conditional( self, restOfLine ) : # unready 12 1 23
		"# if x > y goto #2"
		# verify the rest of the line
		# generate & save instructions for the conditional
		# search for ref line
		SCompiler.searchForSymbol( self, sym )
		# store if found,
		# flag if not
		pass

	def assignment( self, restOfLine ) : # unready 12 1 23
		'form of let x = ( y + 2 ) / 99 * z, so convert no matter what'
		# convert rest to postfix
		# eval postfix :
			# push mem locations
			# save commands rather than evaluating
			# save sub expression in location
			# store that answer
		pass
			
	def firstPass( self, line ) : # tentative, components unready 12 1 23
		segment = line.split( ' ' )
		if not segment[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "line number missing" )
		''' check if this line number is greater than last, else syntax error '''
		# store the line number
		self.currSym += 1
		self.symbolTable[ currSym ].type = SCompiler.LINE
		self.symbolTable[ currSym ].symbol = segment[ 0 ] # in this case, the line number
		comm = segment[ 1 ]
		if comm not in self.commandList :
			SCompiler.syntaxError( self, "unrecognized command " + comm )
		else :
			self.instructionCounter += 1
			if SCompiler.programTooBig( self ) :
				SCompiler.syntaxError( self, "Too many instructions reserved" )
				# unfortunately, an extra remark may temporarily exceed the limit
			self.symbolTable[ self.currSym ].location = self.instructionCounter
			newInstruc = commandList[ comm ]
			SCompiler.newInstruc( self, segment[ 1: ] ) #cut line number & command
	
	def resolveForwardReferencedLines( self ) :# WORKING HERE 12 1 23
		# WAS self.lineFlags[ self.instructionCounter ] = referencedLineNumber
		ind = 0
		limit = len( self.lineFlags ) - 1
		while ind <= limit :
			if self.lineFlags[ ind ] >= 0 :
				# find that line number in symbolTable
				#rewrite the goto instruction
				where = SCompiler.searchForSymbol( self, self.lineFlags[ ind ] )
				if self.symbolTable[ where ].type == SCompiler.LINE :
					# resolve
					self.smlData[ ind ] += self.symbolTable[ where ].location
				else :
					SCompiler.syntaxError( self, "referenced line number at " + str( where ) + "not found" )
	
	def secondPass( self ) : # tentative, components unready 12 1 23
		SCompiler.resolveForwardReferencedLines( self )
		output = open( "ex1.sml", 'w' )
		for nn in self.smlData :
			output.write( nn )
		output.close( )
		pass

	def compile( self, simpleFile ) : # tentative, components unready 12 1 23
		simpleProgram = open( simpleFile )
		for line in simpleProgram :
			SCompiler.firstPass( self, line )
		SCompiler.secondPass( self )
		simpleProgram.close( )
# WORKING HERE 12 1 23

# find git remove file from repository
#LOOK ONLINE FOR CMD