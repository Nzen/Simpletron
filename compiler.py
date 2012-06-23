
# Nicholas Prado
# begun 12 1 11
# Compiler/assembler for Deitel's Simple language into SML for the Simpletron

'''	todays notes

'''
import postFixer
import stack
# import symbolTableEntry

class TableEntry( object ) :
	'simple record for each element of the simple values'
	def __init__( self ) :
		self.symbol = ""
		self.type = 0 # line-0, var-1, or constVal-2
		self.location = 0

	def __str__( self ) :
		types = { 0 : "line num", 1 : "variable", 2 : "const num" }
		return str( self.symbol ) + "\t" + types[ self.type ] + "\t" + str( self.location )

class SCompiler( object ) :

	STOP = 0000 # Deitel has a different number. Warford & present technique ensure bad accesses halt the program
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
	FAILED = False # for testing when syntaxError shouldn't exit( )

	def __init__( self ) : # tentative 12 1 23
		self.symbolTable = [ TableEntry( ) ] * SCompiler.RAMSIZE
		self.lineFlags = [ -1 ] * SCompiler.RAMSIZE # notes which fail, only because of spec else I'd use a list
		self.smlData = [ 0 ] * SCompiler.RAMSIZE # floods ram later
		self.instructionCounter = -1
		self.dataCounter = SCompiler.RAMSIZE # sc.RS - 1? 12 3 18
		self.currSym = -1 # index in symbol table of latest
		self.lastLine = -1 # for checkLineNumIncreasing

	def showSymbolTable( self ) :
		print
		print "\n\tContents of Symbol Table"
		print "Current symbol index - "  + str( self.currSym )
		print "sym\ttype\tlocation"
		ind = 0
		limit = self.currSym#self.symbolTable.__len__( )
		while ( ind < limit ) :
			print self.symbolTable[ ind ]
			ind += 1

	def showInterestingLineFlags( self ) :
		'print the lineFlags with forward references only'
		# self.lineFlags[ self.instructionCounter ] = int( self.symbolTable[ lineNumIndex ].symbol )
		print
		print "\tForward referenced lines:"
		ind = 0
		limit = self.lineFlags.__len__( )
		while ind < limit :
			lineNum = self.lineFlags[ ind ]
			if lineNum >= 0 :
				print "line called " + str( lineNum ) + " referenced by instruction in mem " + str( ind )
			ind += 1

	def showMem( self ) :
		print
		print "Instr count - " + str( self.instructionCounter ) + "\tData counter - " + str( self.dataCounter )
		print "\tContents of sml data bank"
		ind = 0
		vert = 0
		#off = 0
		maxVert = 5
		lim = self.smlData.__len__( )
		for yy in range( 0, 5 ) : # should reflect memory size
			print '\t' + str( yy ),
		print
		print '\t',
		while ind < lim :
			if vert >= maxVert :
				vert = 0
				print
				print ( str( ind ) + '\t' ),
			print ( str( self.smlData[ ind ] ).rjust( 4, '0' ) + '\t' ),
			ind += 1
			vert += 1
			#off += 5
	
	def showState( self ) :
		SCompiler.showSymbolTable( self )
		SCompiler.showInterestingLineFlags( self )
		SCompiler.showMem( self )

	def syntaxError( self, why ) : # tentative 12 2 7
		if self.lastLine < 0 :
			self.lastLine = 0 # for human clarity
		print "XX > %s in line %d" % ( why, self.lastLine )
		SCompiler.showState( self )
		if SCompiler.TESTING :
			SCompiler.FAILED = True
		else :
			exit( 1 )

	def checkLineNumbersIncreasing( self, newLineNumber ) : # tentative 12 2 7
		if self.lastLine >= newLineNumber :
			SCompiler.syntaxError( self, "line number " + str( newLineNumber ) + \
			" not greater than previous, " + str( self.lastLine ) )
		else :
			self.lastLine = newLineNumber # for next time

	def validateCommandType( self, word ) : # test validates 12 2 7
		'tests static dict for supplied'
		if word not in SCompiler.commandList :
			SCompiler.syntaxError( self, "unrecognized command " + word )

	def programTooBig( self ) : # tentative 12 1 23
		'instructions build down, data builds up. should the twain meet, Ram is full'
		return self.instructionCounter >= self.dataCounter

	def prepInstruction( self ) : # tentative 12 2 8
		'starting from 0, reserves spot, checks if instructions & data collide'
		self.instructionCounter += 1
		# unfortunately, an extra remark may temporarily exceed the limit, oh well.
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many instructions reserved" )

	def prepDataLocation( self ) : # tentative 12 2 8 or so
		'starting from RamSize, reserves spot, checks if instructions & data collide'
		self.dataCounter -= 1
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many variables, stack overflow" )

	def searchForSymbol( self, sought, typeSought, reserve ) : # tentative 12 2 1
		'returns index in symbolTable or -1 if not present'
		ind = 0
		limit = self.currSym
		while ind <= limit :
			if self.symbolTable[ ind ].symbol == sought :
				if self.symbolTable[ ind ].type == tyepSought : # ensures lineNum & constNum don't conflict
					return ind
			ind += 1
		if reserve : # didn't find the symbol, save new?
			return SCompiler.reserveNewSymbol( self, sought, typeSought )
		else :
			return -1
	
	def reserveNewSymbol( self, symb, theType ) : # tentative 12 2 1
		'reserves new symbol in symbolTable & potentially in dataCounter, returns index in symbolTable'
		self.currSym += 1
		self.symbolTable[ self.currSym ].type = theType
		# numerical symbols are typecast
		self.symbolTable[ self.currSym ].symbol = symb # int( symb ) if symb.isdigit( ) else // Doing it below, watch for bugs
		if theType != SCompiler.LINE :
			SCompiler.prepDataLocation( self )
			self.symbolTable[ self.currSym ].location = self.dataCounter
			if isinstance( symb, int ) : # unidiomatic, FIX this, probably by extracting; and yet, polymorphism is valid
				self.smlData[ self.dataCounter ] = self.symbolTable[ self.currSym ].symbol
			# variables are already initialized to 0 & updated by let or input.
		# line numbers handled by the instruction & firstPass
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
		# remarks don't generate instructions, hence reset IC
		if self.instructionCounter >= 0 :
			self.symbolTable[ self.currSym ].location = self.instructionCounter
			# instead they point at the last legit instruction
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
		whereInd = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		self.smlData[ self.instructionCounter ] = SCompiler.READ + self.symbolTable[ whereInd ].location

	def saveNonLine( self, symbol ) : # tentative 12 2 1
		'returns symbolTable index of saved for consts & vars'
		symType = SCompiler.getType( self, symbol )
		if symType == SCompiler.CONST :
			index = SCompiler.searchForSymbol( self, int( symbol ), type, SCompiler.RESERVE )
		else :
			index = SCompiler.searchForSymbol( self, symbol, type, SCompiler.RESERVE )
		return index

	def screenOutput( self, restOfLine ) : # hmm? 12 6 19
		"# print x" # or a number, if you are silly
		whereInd = SCompiler.saveNonLine( self, restOfLine[ 0 ] )
		self.smlData[ self.instructionCounter ] = SCompiler.WRITE + self.symbolTable[ whereInd ].location

	def goto( self, opType, lineNumIndex, lineNumDefined ) : # tentative 12 2 8
		'the logic was backwards here'
		if lineNumDefined :
			self.smlData[ self.instructionCounter ] = opType + self.symbolTable[ lineNumIndex ].location
		else :
			# flag for later substitution // does IC point to the correct one here?
			self.lineFlags[ self.instructionCounter ] = int( self.symbolTable[ lineNumIndex ].symbol )
			# write tentative goto
			self.smlData[ self.instructionCounter ] = opType # points at 3X00

	def symbFound( self, index ) :  # ok 12 2 8
		'ie a line number is in this index of lineFlags'
		return index >= 0

	def branch( self, restOfLine ) : # FIX 12 2 8
		"#1 goto #2"
		if not restOfLine[ 0 ].isdigit( ) :	# POINTS AT Index or resolving is failing
			SCompiler.syntaxError( self, "can not jump to variable value " + \
			restOfLine[ 0 ] + ", only to integer line numbers" )
		# search symbolTable for the referenced line number
		whereIndex = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTO, whereIndex, SCompiler.symbFound( self, whereIndex ) )

	def simulateOrEquals( self ) : # tentative 12 2 8
		'subtract one more to push an equals to neg'
		# given x>y, y-x < 0; if I want x>=y then y-x may = 0
		indOfOne = SCompiler.searchForSymbol( self, 1, SCompiler.CONST, SCompiler.RESERVE )
		SCompiler.prepInstruction( self )
		self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ indOfOne ].location

	def conditionalProduction( self, firstInd, secondInd, orEqual ) : # tentative 12 2 8
			'loads first, subtracts second; IF orEqualTo subtracts one more, so gotoNeg works'
			# save: load first to acc
			self.smlData[ self.instructionCounter ] = SCompiler.LOAD + self.symbolTable[ firstInd ].location
			# save: subtract second from first
			SCompiler.prepInstruction( self )
			self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ secondInd ].location
			if orEqual :
				SCompiler.simulateOrEquals( self )

	def validateIfgotoExpression( self, expression ) : # mhmm 12 6 19
		'x > y goto #'
		conditionals = ( "==", ">=", "<=", ">", "<" )
		numSymb = len( expression )
		if numSymb < 5 :
			SCompiler.syntaxError( self, "Not enough symbols in the 'if goto' command" )
		elif numSymb > 5 :
			SCompiler.syntaxError( self, "Too many symbols in the 'if goto' command" )
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

	def relationConditional( self, whereX, whereY, lineNumSymb ) :
		'uses gotoNeg rather than zero; comparison fsm ensures sensible subtractions'
		orEquals = True
		if comparison == ">=" :
			SCompiler.conditionalProduction( self, whereY, whereX, orEquals )
		elif comparison == "<=" :
			SCompiler.conditionalProduction( self, whereX, whereY, orEquals )
		elif comparison == ">" :
			SCompiler.conditionalProduction( self, whereY, whereX, not orEquals )
		else : # must be "<"
			SCompiler.conditionalProduction( self, whereX, whereY, not orEquals )
		# resolve goto
		whereLine = SCompiler.searchForSymbol( self, restOfLine[ 4 ], SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTONEG, whereLine, SCompiler.symbFound( self, whereLine ) )
	
	def conditional( self, restOfLine ) : # FIX 12 2 8
		"# if x > y goto #2"
		SCompiler.validateIfgotoExpression( self, restOfLine )
		whereX = SCompiler.saveNonLine( self, restOfLine[ 0 ] )
		comparison = restOfLine[ 1 ]
		whereY = SCompiler.saveNonLine( self, restOfLine[ 2 ] )
		# resolve conditional expression
		if comparison == "==" :
			SCompiler.conditionalProduction( self, whereX, whereY, False ) # not orEquals
			whereLine = SCompiler.searchForSymbol( self, restOfLine[ 4 ], SCompiler.LINE, not SCompiler.RESERVE )
			SCompiler.goto( self, SCompiler.GOTOZERO, whereLine, SCompiler.symbFound( self, whereLine ) ) ## points at data section
		else :
			SCompiler.relationConditional( self, whereX, whereY, restOfLine[ 4 ] )

	def checkFirstTwoChars( self, varNequal ) : # tentative 12 2 8
		if varNequal[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Can't assign new values to numbers" )
		elif varNequal[ 1 ] is not "=" :
			SCompiler.syntaxError( self, "Expected '=' after assignment target " + varNequal[ 0 ] )
		
	def checkForUnexpected( self, expression ) : # tentative 12 2 8
		'realistically, I should determine the alternating nature of the expression. Later' # ( ( ( x - 5 / x ) + z ) ) - a
		# # pair parenthises => x - 5 / x + z - a ; check alternating alnum operator
		'''
		ind = 0
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
						SCompiler.syntaxError( self, "You put a zero as a denominator" ) 
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
		SCompiler.checkFirstTwoChars( self, restOfLine[ :2 ] ) # that's not consistent slicing syntax, Guido
		SCompiler.checkForUnexpected( self, restOfLine[ 2: ] )
		indexFinal = SCompiler.searchForSymbol( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		decrypted = postFixer.convertToPostFix( restOfLine[ 2: ], False ) # cut x = ;; convert not verbosely
		penultimateLocation = SCompiler.evaluatePostFix( self, decrypted ) # mixing locations & symTab indexes is weird
		# penultimate into acc
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + penultimateLocation
		SCompiler.prepInstruction( self )
		# store into whereFinal
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + self.symbolTable[ indexFinal ].location

	def prepThisLinesNumber( self, lineNumber ) :
		'save the line number in symbolTable; since increasing, dont search'
		if not lineNumber.isdigit( ) :
			SCompiler.syntaxError( self, "First symbol must be a line number" )
		SCompiler.checkLineNumbersIncreasing( self, int( lineNumber ) )
		SCompiler.reserveNewSymbol( self, lineNumber, SCompiler.LINE )
		return self.currSym
	
	def firstPass( self, line ) : # tentative 12 2 7
		'validate/prep lineNum, prep next Instruction, call command( )'
		segment = line.split( ' ' )
		lineNumber = segment[ 0 ]
		whereLine = SCompiler.prepThisLinesNumber( self, lineNumber )
		comm = segment[ 1 ]
		SCompiler.validateCommandType( self, comm )
		SCompiler.prepInstruction( self )
		self.symbolTable[ whereLine ].location = self.instructionCounter
		newInstruc = SCompiler.commandList[ comm ] # string of the function name
		newInstruc( self, segment[ 2: ] ) # cut line number & command, send restOfLine

	def resolveForwardReferencedLines( self ) : # REVIEW OR FIX 12 2 8
		'lineFlags are initialized to -1; forward references contain lineNumber (ie symbol) pointed at'
		# Resolves self.lineFlags[ self.instructionCounter ] = int( self.symbolTable[ lineNumIndex ].symbol )
		##SCompiler.showInterestingLineFlags( self )
		ind = 0
		limit = SCompiler.RAMSIZE # limit of lineFlags array // shouldn't the limit be instructionCounter? I don't want to change vars
		while ind < limit :
			lineNum = self.lineFlags[ ind ]
			if lineNum >= 0 :
				# find that line number in symbolTable
				whereInd = SCompiler.searchForSymbol( self, lineNum, SCompiler.LINE, not SCompiler.RESERVE )
				# resolve
				if not SCompiler.symbFound( self, whereInd ) :
					SCompiler.syntaxError( self, "referenced line number at " + str( lineNum ) + " not found" )
				else :
					self.smlData[ ind ] += self.symbolTable[ whereInd ].location # was 4100, now 41xx
			ind += 1

	def saveProgram( self, originalFileName ) : # tentative 12 2 8
		'write to filename.sml # return that name'
		newFileName = originalFileName[ : -3 ] + "sml" # replaces .txt or similar
		output = open( newFileName, 'w' )
		output.truncate( ) # erase what's in there for safety
		for nn in self.smlData :
			output.write( str( nn ) + '\n' ) # consider using same technique as Ram.coreDump
		output.close( )
		return newFileName
		'''	coreDump( )
		endl = 0
		for yy in range( 0, 10 ) : # should reflect memory size, say ramSize / 10
			dumpSite.write( '\t' + str( yy ) )
		for nn in self.memory:
			if 0 == endl % 10 :
				dumpSite.write( '\n' + str( endl ) + '\t' ) # 00xx
			dumpSite.write( str( nn ).rjust( 4, '0' ) + '\t' ) # doesn't need to be \n\r
			endl += 1
		'''

	def secondPass( self, originalFileName ) : # tentative 12 2 8
		'resolve goto statements, print to x.sml return that filename'
		SCompiler.resolveForwardReferencedLines( self )
		return SCompiler.saveProgram( self, originalFileName )

	def compile( self, simpleFile ) : # tentative 12 2 8
		'compiles or reports syntaxError, returns name of new sml file to run'
		simpleProgram = open( simpleFile )
		for line in simpleProgram :
			SCompiler.firstPass( self, line.rstrip( '\n' ) )
			#print ". Line complete"
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