
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

	def prepInstruction( self ) : # tentative 12 2 8
		self.instructionCounter += 1
		# unfortunately, an extra remark may temporarily exceed the limit
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many instructions reserved" )

	def prepDataLocation( self ) :
		self.dataCounter -= 1
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many variables, stack overflow" )

	def searchForSymbol( self, sought, typeSought, reserve ) : # tentative 12 2 1
		'returns index in symbolTable or -1 if not present'
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
		'reserves new symbol in symbolTable & potentially in dataCounter, returns index in symbolTable'
		self.currSym += 1
		self.symbolTable[ self.currSym ].type = theType
		# numerical symbols are typecast
		self.symbolTable[ self.currSym ].symbol = int( symb ) if symb.isdigit( ) else symb # given use case, waste?
		if theType is not SCompiler.LINE :
			SCompiler.prepDataLocation( self )
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

	def userInput( self, restOfLine ) : # seems to work 12 2 8
		"# input x (meaning) store input in var x"
		if restOfLine[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Simple will not use numbers (" + restOfLine[ 0 ] + ") as variable names" )
		where = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		self.smlData[ self.instructionCounter ] = SCompiler.READ + self.symbolTable[ where ].location

	def screenOutput( self, restOfLine ) : # FIX 12 2 8
		"# print x" # or a number
		symType = SCompiler.getType( self, restOfLine[ 0 ] )	# POINTS AT AN INSTRUCTION
		where = SCompiler.searchForSymbol( self, restOfLine[ 0 ], symType, not SCompiler.RESERVE )
		self.smlData[ self.instructionCounter ] = SCompiler.WRITE + self.symbolTable[ where ].location

	def validateIfgotoExpression( self, expression ) : # tentative 12 2 8
		'x > y goto #'
		conditionals = ( "==", ">=", "<=", ">", "<" )
		if len( expression ) < 4 :
			SCompiler.syntaxError( self, "Not enough symbols in if goto command" )
		elif not expression[ 0 ].isalnum( ) :
			SCompiler.syntaxError( self, "First symbol in a comparison must be a number or letter" )
		elif expression[ 1 ] not in conditionals :
			SCompiler.syntaxError( self, "Second symbol in a conditional must be an operator: >, <, ==, >=, <=" )
		elif not expression[ 2 ].isalnum( ) :
			SCompiler.syntaxError( self, "Third symbol in a comparison must be a number or letter" )
		elif expression[ 3 ] != "goto" :
			SCompiler.syntaxError( self, "The goto command must follow the if's conditional expression" )
		elif not expression[ 4 ].isdigit( ) :
			SCompiler.syntaxError( self, "goto must be followed by a line number" )
		else :
			return # I just like completing the elif field

	def found( self, index ) :  # ok 12 2 8
		return index >= 0

	def goto( self, opType, lineNumIndex, unresolved ) : # tentative 12 2 8
		'again I"ve run into the symTable/instrCount ambiguity of lineNumIndex'
		if unresolved :
			# flag for later substitution
			self.lineFlags[ self.instructionCounter ] = self.symbolTable[ lineNumIndex ].symbol # only place where numeric casting important
			# write tentative goto
			self.smlData[ self.instructionCounter ] = opType # points at 00
		else :
			self.smlData[ self.instructionCounter ] = opType + self.symbolTable[ lineNumIndex ].location

	def branch( self, restOfLine ) : # FIX 12 2 8
		"#1 goto #2"
		if not restOfLine[ 0 ].isdigit( ) :	# POINTS AT ITSELF?? maybe index? or resolving is failing
			SCompiler.syntaxError( self, "can not jump to variable value line, only constants" )
		# search symbolTable for the referenced line number
		index = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTO, index, SCompiler.found( self, index ) )

	def saveNonLine( self, symbol ) : # tentative 12 2 1
		'returns symbolTable index of saved'
		type = SCompiler.getType( self, symbol )
		index = SCompiler.searchForSymbol( self, symbol, type, SCompiler.RESERVE )
		return index

	def simulateOrEquals( self ) : # tentative 12 2 8
		where = SCompiler.searchForSymbol( self, "1", SCompiler.CONST, SCompiler.RESERVE )
		SCompiler.prepInstruction( self )
		self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ where ].location

	def conditionalProduction( self, first, second, orEqual ) : # tentative 12 2 8
			'loads first, subtracts second, subtracts another if orEqualTo appropriate'
			# save: load first to acc
			self.smlData[ self.instructionCounter ] = SCompiler.LOAD + self.symbolTable[ first ].location
			# save: subtract second from first
			SCompiler.prepInstruction( self )
			self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ second ].location
			if orEqual :
				SCompiler.simulateOrEquals( self )

	def conditional( self, restOfLine ) : # FIX 12 2 8
		"# if x > y goto #2"
		orEquals = True
		SCompiler.validateIfgotoExpression( self, restOfLine )
		whereX = SCompiler.saveNonLine( self, restOfLine[ 0 ] )
		comparison = restOfLine[ 1 ]
		whereY = SCompiler.saveNonLine( self, restOfLine[ 2 ] )
		# resolve conditional expression
		if comparison == "==" :
			SCompiler.conditionalProduction( self, whereX, whereY, orEquals ) ## this didn't emit a gotozero
			whereLine = SCompiler.searchForSymbol( self, restOfLine[ 4 ], SCompiler.LINE, not SCompiler.RESERVE )
			SCompiler.goto( self, SCompiler.GOTOZERO, whereLine, SCompiler.found( self, whereLine ) ) ## points at data section
			return # avoids common code at bottom
		elif comparison == ">=" :
			SCompiler.conditionalProduction( self, whereY, whereX, orEquals )
		elif comparison == "<=" :
			SCompiler.conditionalProduction( self, whereX, whereY, orEquals )
		elif comparison == ">" :
			SCompiler.conditionalProduction( self, whereY, whereX, not orEquals )
		else : # must be "<"
			SCompiler.conditionalProduction( self, whereX, whereY, not orEquals )
		# resolve goto
		whereLine = SCompiler.searchForSymbol( self, restOfLine[ 4 ], SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTONEG, whereLine, SCompiler.found( self, whereLine ) )

	def checkFirstTwoChars( self, varNequal ) : # tentative 12 2 8
		if varNequal[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Can't assign new values to numbers" )
		elif varNequal[ 1 ] is not "=" :
			SCompiler.syntaxError( self, "Expected '=' after assignment target " + varNequal[ 0 ] )
		
	def checkForUnexpected( self, expression ) : # tentative 12 2 8
		'realistically, I should determine the alternating nature of the expression. Later' # ( ( ( x - 5 / x ) + z ) ) - a
		'''	ind = 0
		lim = len( expression ) # yak shaving?
		worked = True
		while ind <= lim : # FSM oooh, what regex facilities does python have?
			if expression[ ind ].isalnum( ) :
				ind += 1
				worked = True
			elif expression[ ind ] is '(' or expression[ ind ] is ')' : # postfix can handle matching, if it does
				ind += 1
				worked = True
			else :
				worked = False
				break
			if expression[ ind ] in operators :
				ind += 1
				worked = True
			else :
				SCompiler.syntaxError( self, "Invalid symbol in expression " + ex ) # or I didn't expect it
			'''	# I'll figure out something eventually
		#
		operators = [ '+', '-', '*', '/', '(', ')' ]
		for ex in expression :
			if ex.isalnum( ) :
				continue
			elif ex in operators :
				continue
			else :
				SCompiler.syntaxError( self, "Invalid symbol in expression " + ex )

	def spotForTempAnswer( self ) : # tentative 12 2 8
		SCompiler.prepDataLocation( self )
		return self.dataCounter

	def mathProduction( self, whereY, operator, whereX ) : # tentative 12 2 8
		'calls Y to acc, applys operator with X to acc, stores result'
		# Y into accumulator
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + whereY
		SCompiler.prepInstruction( self )
		# apply X to accumulator
		self.smlData[ self.instructionCounter ] = operator + whereX
		SCompiler.prepInstruction( self )
		# store acc into new spot
		tempLocation = SCompiler.spotForTempAnswer( self )
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + tempLocation
		SCompiler.prepInstruction( self ) # for the next pass or final storage
		return tempLocation # returning location because there is no symbol
		
	def checkDenominator( self, whereDenominator ) : # tentative 12 2 8
		"unreliable means of checking if denominator is 0"
		"""
		In fact, there is no way (halting problem) that I can check at compile time whether
		the denominator is surely 0 without evaluating the program. A const denominator is
		safe, but any variable is initialized to 0. I would have to keep track of variables
		changed in let or input statements ( & input could be zero again ) and flag any that weren't.
		"""
		ind = 0
		limit = self.currSym
		while ind <= limit :
			if self.symbolTable[ ind ].location is whereDenominator : # how much overlap is possible?
				if self.symbolTable[ ind ].type is SCompiler.CONST :
					if self.symbolTable[ ind ].symbol is not 0 :
						return # safe denominator
					else :
						SCompiler.syntaxError( self, "You put a zero as a denominator" ) # unfortunately, I can't tell you which char it is from in here
				else : # is a variable
					# compromise since it could be anything.
					print "Warning: potential zero denominator at line %d" % self.lastLine
					return
			ind += 1

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

	def evaluatePostFix( self, postfix ) : # tentative 12 2 8
		' convert polish equation to SML instructions & mem reservations '
		tempVals = stack.Stack( )
		ind = 0 # was name conflicting with indecies below
		y = 0
		x = 0
		postfix.append( ">" ) # sentinel
		focus = postfix[ ind ]
		while ">" is not focus :
			if focus.isdigit( ) :
				index = SCompiler.searchForSymbol( self, focus, SCompiler.CONST, SCompiler.RESERVE )
				where = self.symbolTable[ index ].location
				tempVals.push( where )
			elif focus.isalpha( ) :
				index = SCompiler.searchForSymbol( self, focus, SCompiler.VAR, SCompiler.RESERVE )
				where = self.symbolTable[ index ].location
				tempVals.push( where )
			else : # isOperator( )
				x = tempVals.pop( )
				y = tempVals.pop( )
				tempLocation = SCompiler.evaluateCode( self, y, focus, x )
				tempVals.push( tempLocation )
			ind += 1
			focus = postfix[ ind ]
		return tempVals.pop( ) # answer location

	def assignment( self, restOfLine ) : # tentative 12 2 8
		'form of let x = ( y + 2 ) / 99 * z'
		SCompiler.checkFirstTwoChars( self, restOfLine[ :2 ] ) # that's not consistent slicing
		SCompiler.checkForUnexpected( self, restOfLine[ 2: ] )
		indexFinal = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		decrypted = postFixer.convertToPostFix( restOfLine[ 2: ], False ) # cut x = ;; convert not verbosely
		penultimateLocation = SCompiler.evaluatePostFix( self, decrypted )
		# penultimate into acc
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + penultimateLocation
		SCompiler.prepInstruction( self )
		# store into whereFinal
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + self.symbolTable[ indexFinal ].location
			
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
		SCompiler.prepInstruction( self )
		self.symbolTable[ self.currSym ].location = self.instructionCounter
		newInstruc = SCompiler.commandList[ comm ]
		newInstruc( self, segment[ 2: ] ) #cut line number & command
	
	def resolveForwardReferencedLines( self ) : # REVIEW OR FIX 12 2 8
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
					SCompiler.syntaxError( self, "referenced line number at " + str( where ) + "not found" ) # may not have worked?
				else :
					self.smlData[ ind ] += self.symbolTable[ where ].location # was 4100, now 41xx
			ind += 1

	def saveProgram( self, originalFileName ) : # tentative 12 2 8
		'write to filename.sml # return that name'
		newFileName = originalFileName[ : -4 ] + ".sml" # replaces .txt or similar
		output = open( newFileName, 'w' )
		output.truncate( ) # erase what's in there for safety
		for nn in self.smlData :
			output.write( str( nn ) + '\n' )
		output.close( )
		return newFileName

	def secondPass( self, originalFileName ) : # tentative 12 2 8
		'resolve goto statements, print to x.sml return that filename'
		SCompiler.resolveForwardReferencedLines( self )
		return SCompiler.saveProgram( self, originalFileName )

	def compile( self, simpleFile ) : # tentative 12 2 8
		simpleProgram = open( simpleFile )
		for line in simpleProgram :
			SCompiler.firstPass( self, line.rstrip( '\n' ) )
		simpleProgram.close( )
		#
		newFile =  SCompiler.secondPass( self, simpleFile )
		print "done"
		return newFile
		
	commandList = {
		"end" : finished,
		"rem" : comment,
		"let" : assignment,
		"if" : conditional,
		"goto" : branch,
		"input" : userInput,
		"print" : screenOutput,
		}