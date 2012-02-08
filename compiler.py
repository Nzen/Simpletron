
# Nicholas Prado
# begun 12 1 11
# Compiler/assembler for Deitel's Simple language into SML for the Simpletron

import postFixer
import stack
# import symbolTableEntry

class TableEntry( object ) : # tentative 12 1 23
	'simple record for each element of the simple values'
	def __init__( self ) :
		self.symbol = ""
		self.type = 0 # line var or constVal
		self.location = 0

class SCompiler( object ) :

	STOP = 0000
	READ = 1000
	WRITE = 1100
	ADD = 2000
	SUBTR = 2100
	MULTP = 2200
	DIVIDE = 2300
	GOTO = 3000
	GOTOZERO = 3100
	GOTONEG = 3200
	LOAD = 4000
	STORE = 4100
	RAMSIZE = 100
	LINE = 0
	VAR = 1
	CONST = 2
	RESERVE = True
	TESTING = False
	FAILED = False # for testing when syntaxError doesn't exit( )

	def __init__( self ) : # tentative 12 1 23
		self.symbolTable = [ TableEntry( ) ] * SCompiler.RAMSIZE
		self.lineFlags = [ -1 ] * SCompiler.RAMSIZE
		self.smlData = [ 0 ] * SCompiler.RAMSIZE
		self.instructionCounter = -1
		self.dataCounter = SCompiler.RAMSIZE
		self.currSym = -1
		self.lastLine = -1
		
	def syntaxError( self, why ) : # tentative 12 2 7
		if self.lastLine < 0 :
			self.lastLine = 0 # for human clarity
		print "%s in line %d" % ( why, self.lastLine )
		if SCompiler.TESTING :
			SCompiler.FAILED = True
		else :
			exit( 1 )

	def checkLineNumbersIncreasing( self, newLineNumber ) : # tentative 12 2 7
		if self.lastLine >= newLineNumber :
			SCompiler.syntaxError( self, "line number " + str( newLineNumber ) + " not above previous" )
		else :
			self.lastLine = newLineNumber

	def validateCommandType( self, word ) : # test validates 12 2 7
		'tests static dict for supplied'
		if word not in SCompiler.commandList :
			SCompiler.syntaxError( self, "unrecognized command " + word )

	def programTooBig( self ) : # tentative 12 1 23
		'instructions build down, data builds up. should the twain meet, Ram is full'
		return self.instructionCounter >= self.dataCounter

	def searchForSymbol( self, sought, typeSought, reserve ) : # tentative 12 2 1
		'returns index of symbol or -1 if not present'
		ind = 0
		limit = self.currSym
		while ind <= limit :
			if self.symbolTable[ ind ].symbol == sought :
				if self.symbolTable[ ind ].type == tyepSought :
					return ind
			ind += 1
		if reserve :
			return SCompiler.reserveNewSymbol( self, sought, typeSought )
		else :
			return -1
	
	def reserveNewSymbol( self, symb, theType ) : # tentative 12 2 1
		'reserves new symbol in symbolTable & potentially in dataCounter, returns index'
		self.currSym += 1
		self.symbolTable[ self.currSym ].type = theType
		# numerical symbols are typecast
		self.symbolTable[ self.currSym ].symbol = int( symb ) if symb.isdigit( ) else symb # given useCase, waste?
		self.dataCounter -= 1
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many variables reserved: " + symb )
		self.symbolTable[ self.currSym ].location = self.dataCounter
		if symb.isdigit( ) :
			self.smlData[ self.dataCounter ] = self.symbolTable[ self.currSym ].symbol
		# variables are initialized to 0 & updated by let or input.
		return self.currSym
		
	def getType( self, unknown ) : # tentative 12 1 28
		'Only for var & const. Instances of line numbers are invariant'
		if unknown.isdigit( ) :
			return SCompiler.CONST
		else :
			return SCompiler.VAR
			
	def comment( self, restOfLine ) : # tentative 12 1 28
		"# remark lorem ipsum dolores set amet"
		self.instructionCounter -= 1
		# remarks don't generate instructions, hence reset
		if self.instructionCounter >= 0 :
			self.symbolTable[ self.currSym ].location = self.instructionCounter
		else :
			self.symbolTable[ self.currSym ].location = 0
		# but the first time IC is -1 rather than 0, so leaving it thus would underflow
		# if a goto pointed at it. I'd like to optimize this into a single check but not now.
		pass # this pass & similars are because notepad++ doesn't fold the comments below a function

	def finished( self, restOfLine ) : # tentative 12 1 23
		"# halt"
		self.smlData[ self.instructionCounter ] = SCompiler.STOP

	def userInput( self, restOfLine ) : # tentative 12 1 28
		"# input x (meaning) store input in var x"
		if restOfLine[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Simple will not use numbers (" + restOfLine[ 0 ] + ") as variable names" )
		where = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		self.smlData[ self.instructionCounter ] = SCompiler.READ + self.symbolTable[ where ].location

	def screenOutput( self, restOfLine ) : # tentative 12 1 28
		"# print x" # also, print a #, however all variables are initialized to 0 so be wary
		symType = SCompiler.getType( self, restOfLine[ 0 ] )
		where = SCompiler.searchForSymbol( self, restOfLine[ 0 ], symType, not SCompiler.RESERVE ) ##seems okay, rewrite these
		self.smlData[ self.instructionCounter ] = SCompiler.WRITE + self.symbolTable[ where ].location

	def found( self, index ) :  # ok 12 1 28
		return index >= 0

	def goto( self, opType, lineNumIndex, unresolved ) : # tentative 12 2 1
		'again I"ve run into the symTable/instrCount ambiguity of lineNumIndex'
		if unresolved :
			# flag for later substitution
			self.lineFlags[ self.instructionCounter ] = self.symbolTable[ lineNumIndex ].symbol # only place where numeric casting important
			# write tentative goto
			self.smlData[ self.instructionCounter ] = opType # points at 00
		else :
			self.smlData[ self.instructionCounter ] = opType + self.symbolTable[ lineNumIndex ].location

	def branch( self, restOfLine ) : # tentative 12 2 1
		"#1 goto #2"
		if not restOfLine[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "can not jump to variable value line, only constants" )
		# search symbolTable for the referenced line number
		where = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTO, where, found( where ) )

	def prepInstruction( self ) : # tentative 12 2 1
		self.instructionCounter += 1
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many instructions reserved" )

	def saveNonLine( self, symbol ) : # tentative 12 2 1
		'returns symbolTable index of saved'
		firstType = SCompiler.getType( self, symbol )
		whereX = SCompiler.searchForSymbol( self, symbol, firstType, SCompiler.RESERVE )

	def simulateOrEquals( self ) : # tentative 12 2 1
		where = SCompiler.searchForSymbol( self, 1, SCompiler.CONST, SCompiler.RESERVE )
		SCompiler.prepInstruction( self )
		self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ where ].location

	def conditionalProduction( self, first, second, orEqual ) : # tentative 12 2 1
			'loads first, subtracts second, subtracts another if orEqualTo appropriate'
			# save: load first to acc
			self.smlData[ self.instructionCounter ] = SCompiler.LOAD + self.symbolTable[ first ].location
			# save: subtract second from first
			SCompiler.prepInstruction( self )
			self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ second ].location
			if orEqual :
				SCompiler.simulateOrEquals( self )

	def conditional( self, restOfLine ) : # tentative 12 2 5
		"# if x > y goto #2"
		SCompiler.validateRestExpression( self, restOfLine )
		whereX = SCompiler.saveNonLine( self, restOfLine[ 0 ] )
		comparison = restOfLine[ 1 ]
		whereY =  SCompiler.saveNonLine( self, restOfLine[ 2 ] )
		# resolve conditional expression
		if comparison == "==" :
			SCompiler.conditionalProduction( self, whereX, whereY, FALSE )
			whereLine = SCompiler.searchForSymbol( self, restOfLine[ 4 ], SCompiler.LINE, not SCompiler.RESERVE )
			SCompiler.goto( self, SCompiler.GOTOZERO, whereLine, found( whereLine ) )
			return # avoids common code at bottom
		elif comparison == ">=" :
			SCompiler.conditionalProduction( self, whereY, whereX, TRUE ) # "or Equals"
		elif comparison == "<=" :
			SCompiler.conditionalProduction( self, whereX, whereY, TRUE ) # "or Equals"
		elif comparison == ">" :
			SCompiler.conditionalProduction( self, whereY, whereX, FALSE ) # not "or Equals"
		else : # must be "<"
			SCompiler.conditionalProduction( self, whereX, whereY, FALSE ) # not "or Equals"
		# resolve goto
		whereLine = SCompiler.searchForSymbol( self, restOfLine[ 4 ], SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTONEG, whereLine, found( whereLine ) )
		
	def checkForUnexpected( self, restOfLine ) : # tentative 12 2 7
		'realistically, I should determine the alternating nature of the expression. Later'
		operators = [ '+', '-', '*', '/', '(', ')' ]
		for ex in restOfLine :
			if ex.isalnum( ) :
				continue
			elif ex in operators :
				continue
			else :
				SCompiler.syntaxError( self, "Invalid symbol in expression " + ex )

	def mathProduction( self, whereY, operator, whereX ) : # tentative 12 2 7
		'calls Y to acc, applys operator with X to acc, stores result'
		# Y into accumulator
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + whereY
		self.instructionCounter += 1
		# apply X to accumulator
		self.smlData[ self.instructionCounter ] = operator + whereX
		self.instructionCounter += 1
		# store acc into new spot
		self.currSym += 1
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + self.currSym
		self.instructionCounter += 1 # for the next pass or final storage
		return self.currSym
		pass
		
	def checkDenominator( self, whereDenominator ) : # tentative 12 2 7
		"unreliable means of checking if denominator is 0"
		"""
		In fact, there is no way (halting problem) that I can check at compile time
		whether the denominator is surely 0 without evaluating the program. A const
		denominator is safe, but any variable is initialized to 0. I would have to keep track of variables
		changed in let or input statements ( & input could be zero again ) and flag any that weren't.
		"""
		ind = 0
		limit = self.currSym
		while ind <= limit :
			if self.symbolTable[ ind ].location == whereDenominator :
				if self.symbolTable[ ind ].type == SCompiler.CONST :
					return # safe denominator
				else : # is a variable
					# compromise
					print "Warning: potential zero denominator at line %d" % self.lastLine

	def evaluateCode( self, whereY, operator, whereX ) : # tentative 12 2 7
		'produces production operations for the computation, returns location of result'
		if '+' is operator :
			return SCompiler.mathProduction( self, whereY, SCompiler.ADD, whereX )
		elif '-' is operator :
			return SCompiler.mathProduction( self, whereY, SCompiler.SUBTR, whereX )
		elif '*' is operator :
			return SCompiler.mathProduction( self, whereY, SCompiler.MULTP, whereX )
		elif '/' is operator :
			SCompiler.checkDenominator( self, whereX )
			return SCompiler.mathProduction( self, whereY, SCompiler.DIVIDE, whereX )
		else :
			pass# assert: unreachable

	def evaluatePostFix( self, postfix ) : # tentative 12 2 7
		' convert polish equation to SML instructions & mem reservations '
		tempVals = stack.Stack( )
		index = 0
		y = 0
		x = 0
		postfix.append( ">" ) # sentinel
		focus = postfix[ index ]
		while ">" != focus :
			if focus.isdigit( ) :
				where = SCompiler.searchForSymbol( self, focus, SCompiler.CONST, SCompiler.RESERVE )
				tempVals.push( where )
			elif focus.isalpha( ) :
				where = SCompiler.searchForSymbol( self, focus, SCompiler.VAR, SCompiler.RESERVE )
				tempVals.push( where )
			else : # isOperator( )
				x = tempVals.pop( )
				y = tempVals.pop( )
				whereTemp = SCompiler.evaluateCode( self, y, focus, x )
				tempVals.push( whereTemp )
			index += 1
			focus = postfix[ index ]
		return tempVals.pop( ) # answer location

	def assignment( self, restOfLine ) : # tentative 12 2 7
		'form of let x = ( y + 2 ) / 99 * z, so convert no matter what'
		# store first val	# haven't I done this enough times to extract it?
		if restOfLine[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Can't assign new values to numbers" )
		#SCompiler.checkForUnexpected( self, restOfLine[ 2: ] ) ## UNCOMMENT when I strip the last chars of the newline
		whereFinal = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		decrypted = postFixer.convertToPostFix( restOfLine[ 2: ], False ) # cut x = ;; convert not verbosely
		wherePenultimate = SCompiler.evaluatePostFix( self, decrypted )
		# penultimate into acc
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + wherePenultimate
		self.instructionCounter += 1
		# store into whereFinal
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + whereFinal
			
	def firstPass( self, line ) : # tentative 12 2 7
		segment = line.split( ' ' )
		## strip the newline from 
		lineNumber = segment[ 0 ]
		comm = segment[ 1 ]
		if not lineNumber.isdigit( ) :
			SCompiler.syntaxError( self, "line number missing" )
		SCompiler.checkLineNumbersIncreasing( self, int( lineNumber ) )
		# store the line number
		self.currSym += 1
		# SCompiler.checkSymbolTableOverflow( self )
		self.symbolTable[ self.currSym ].type = SCompiler.LINE
		self.symbolTable[ self.currSym ].symbol = int( lineNumber ) # in this case, the line number
		SCompiler.validateCommandType( self, comm )
		self.instructionCounter += 1
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many instructions reserved" )
			# unfortunately, an extra remark may temporarily exceed the limit
		self.symbolTable[ self.currSym ].location = self.instructionCounter
		newInstruc = SCompiler.commandList[ comm ]
		newInstruc( self, segment[ 2: ] ) #cut line number & command
	
	def resolveForwardReferencedLines( self ) : # tentative 12 2 7
		'lineFlags are initialized to -1; forward references contain lineNumber (ie symbol) pointed at'
		# WAS self.lineFlags[ self.instructionCounter ] = referencedLineNumber
		ind = 0
		limit = len( self.lineFlags )
		while ind < limit :
			if self.lineFlags[ ind ] >= 0 :
				# find that line number in symbolTable
				where = SCompiler.searchForSymbol( self, self.lineFlags[ ind ], SCompiler.LINE, not SCompiler.RESERVE )
				# resolve
				if where < 0 :
					SCompiler.syntaxError( self, "referenced line number at " + str( where ) + "not found" )
				else :
					self.smlData[ ind ] += self.symbolTable[ where ].location # was 4100, now 41xx
			ind += 1

	def saveProgram( self ) : # tentative 12 1 24
		output = open( "ex1.sml", 'w' )
		for nn in self.smlData :
			output.write( str( nn ) + '\n' )
		output.close( )

	def secondPass( self ) : # tentative 12 2 7 
		SCompiler.resolveForwardReferencedLines( self )
		SCompiler.saveProgram( self )

	def compile( self, simpleFile ) : # tentative 12 2 7
		simpleProgram = open( simpleFile )
		for line in simpleProgram :
			SCompiler.firstPass( self, line.rstrip( '\n' ) )
		simpleProgram.close( )
		#
		SCompiler.secondPass( self )
		print "done"
		
	commandList = {
		"end" : finished,
		"rem" : comment,
		"let" : assignment,
		"if" : conditional,
		"goto" : branch,
		"input" : userInput,
		"print" : screenOutput,
		}