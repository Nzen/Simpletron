
# Nicholas Prado
# begun 12 1 11
# Compiler/assembler for Deitel's Simple language into SML for the Simpletron

'''	todays notes

	using math.txt
        Contents of Symbol Table        index - 12
sym     type    location
0       line num        0
x       variable        29
0       const num       28
10      line num        1
y       variable        27
5       const num       26
11      line num        4
12      line num        8
13      line num        9
n       variable        25
14      line num        17
15      line num        18
19      line num        19

Instr count - 19        Data counter - 23
        Contents of sml data bank
        0       1       2       3       4
0       2129    2026    3026    2127    2027
5       3029    3026    3028    2129    2027
10      3226    2124    2029    3328    2123
15      3123    2125    1129    1127    1125
20      0000    0000    0000    0000    0000
25      0000    0005    0000    0000    0000    done
Run sml file? y/n -- y
 save Acc (0) into 0
 load Acc with 0 from 0
 add (acc) 0 and 0
 save Acc (0) into 0
 load Acc with 0 from 0
 add (acc) 0 and 0
 add (acc) 0 and 0
 add (acc) 0 and 0
 save Acc (0) into 0
 load Acc with 0 from 0
 divide (acc) 0 by 0
 save Acc (0) into 0
 load Acc with 0 from 0
 multiply (acc) 0 and 0
 save Acc (0) into 0
 subtract (acc) 0 from 0
 save Acc (0) into 0
 print to terminal:  15
 print to terminal:  10
 print to terminal:  0
Halt program

sml disassemb
 0 store acc into 29	# I think it is the check 'if eqInd + 2 == postfix.__len__( ) '
 1 load acc from 26 	# that determines whether to use resolveAcc()
 2 ++ acc & from 26 	# it doesn't, so 0 is supposedly in the acc and stored into x
 3 store acc into 27	# when really, 0 should be loaded into the acc and then stored in 29
 4 load acc from 27
 5 ++ acc & from 29
 6 ++ acc & from 26
 7 ++ acc & from 28
 8 store acc into 29
 9 load acc from 27
 10 * * acc & from 26
 11 store acc into 24
 12 load acc from 29
 13 / / acc & from 28
 14 store acc into 23
 15 - - acc & from 23
 16 store acc into 25
 17 print from 29
 18 print from 27
 19 print from 25

simple program
 0 let x = 0
 10 let y = 5 + 5
 11 let x = x + y + 5 + 0
 12 rem
 13 let n = 5 * y - 0 / x
 14 print x
 15 print y
 19 print n
'''

import postFixer
import stack

class TableEntry( object ) :
	'simple record for each element of the simple values'
	def __init__( self ) :
		self.symbol = ""
		self.type = 0 # line-0, var-1, or constVal-2
		self.location = 0

	def __str__( self ) :
		types = {
			0 : "line num",
			1  : "variable",
			2 : "const num",
			3 : "array",
			4 : "function",
			5 : "phrase"
			} # key literals because cpu.line, et al, not yet defined
		return str( self.symbol ) + "\t" + types[ self.type ] + "\t" + str( self.location )

class SCompiler( object ) :

	READ  = 1000
	WRITE = 1100
	LOAD  = 2000
	STORE = 2100
	ADD = 3000
	SUBTRACT = 3100
	MULTIPLY = 3200
	DIVIDE = 3300
	MODULUS = 3400
	BRANCH  = 4000
	BRANCHZERO = 4100
	BRANCHNEG = 4200
	HALT  = 4300 # Matches spec, but cpu thinks 0 also is stop, as per Warford
	RAMSIZE = 100 # so bad accesses halt safely rather than fail_coreDump()
	#
	LINE = 0
	VAR  = 1
	CONST = 2
	ARRAY = 3
	FUNCT = 4
	PHRASE = 5 # haha, a string
	RESERVE = True
	TESTING = False
	FAILED = False # for testing when syntaxError shouldn't exit( )

	def __init__( self ) :
		self.symbolTable = [ TableEntry( ) for i in range( SCompiler.RAMSIZE ) ]
		# consider appending to symbol table rather than using an index?
		self.lineFlags = [ -1 ] * SCompiler.RAMSIZE
		# notes which fail, only because of spec else I'd append to a tuple or dict
		self.smlData = [ 0 ] * SCompiler.RAMSIZE # floods ram later
		self.instructionCounter = -1
		self.dataCounter = SCompiler.RAMSIZE # sc.RS - 1? 12 3 18
		self.currSym = -1 # index in symbol table of latest
		self.lastLine = -1 # for checkLineNumIncreasing

	def showSymbolTable( self ) :
		print "\n\tContents of Symbol Table\tindex - " + str( self.currSym )
		print "sym\ttype\t\tlocation"
		ind = 0
		limit = self.currSym #self.symbolTable.__len__( )
		while ( ind <= limit ) :
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
		print "\nInstr count - " + str( self.instructionCounter ) + "\tData counter - " \
			+ str( self.dataCounter )
		print "\tContents of sml data bank"
		ind = 0
		vert = 0
		#off = 0
		maxVert = 5
		lim = self.smlData.__len__( )
		# header
		for yy in range( 0, 5 ) : # should reflect memory size
			print '\t' + str( yy ),
		print '\n0\t',
		while ind < lim :
			if vert >= maxVert :
				vert = 0
				print ( '\n' + str( ind ) + '\t' ),
			print ( str( self.smlData[ ind ] ).rjust( 4, '0' ) + '\t' ),
			ind += 1
			vert += 1
			#off += 5
		pass
	
	def showState( self ) :
		SCompiler.showInterestingLineFlags( self )
		SCompiler.showSymbolTable( self )
		SCompiler.showMem( self )

	def syntaxError( self, why ) :
		if self.lastLine < 0 :
			self.lastLine = 0 # for human clarity
		print "\nXX\nXX > Error, %s in line %d\nXX" % ( why, self.lastLine )
		SCompiler.showState( self )
		if SCompiler.TESTING :
			SCompiler.FAILED = True
		else :
			exit( 1 )

	def checkLineNumbersIncreasing( self, newLineNumber ) :
		if self.lastLine >= newLineNumber :
			SCompiler.syntaxError( self, "line number " + str( newLineNumber ) + \
			" not greater than previous, " + str( self.lastLine ) )
		else :
			self.lastLine = newLineNumber # for next time

	def validateCommandType( self, word ) :
		'tests static dict for supplied'
		if word not in SCompiler.commandList :
			SCompiler.syntaxError( self, "unrecognized command " + word )

	def programTooBig( self ) :
		'instructions build down, data builds up. should the twain meet, Ram is full'
		return self.instructionCounter >= self.dataCounter

	def prepInstruction( self ) :
		'starting from 0, reserves spot, checks if instructions & data collide'
		self.instructionCounter += 1
		# unfortunately, an extra remark may temporarily exceed the limit, oh well.
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many instructions reserved" )

	def prepDataLocation( self ) :
		'starting from RamSize, reserves spot, checks if instructions & data collide'
		self.dataCounter -= 1
		if SCompiler.programTooBig( self ) :
			SCompiler.syntaxError( self, "Too many variables, stack overflow" )

	def getSymbolIndex( self, sought, typeSought, reserve ) :
		'returns index in symbolTable or -1 if not present'
		ind = 0
		limit = self.currSym
		while ind <= limit :
			if self.symbolTable[ ind ].type == typeSought : # ensures lineNum & constNum don't conflict
				if self.symbolTable[ ind ].symbol == sought :
					return ind
			ind += 1
		if reserve : # didn't find the symbol, save new?
			return SCompiler.reserveNewSymbol( self, sought, typeSought )
		else :
			return -1

	def reserveNewSymbol( self, symb, theType ) :
		'reserves new symbol in symbolTable & potentially in dataCounter, returns index in symbolTable'
		# consider appending to symbol table rather than using an index?
		self.currSym += 1
		symInd = self.currSym
		self.symbolTable[ symInd ].type = theType
		self.symbolTable[ symInd ].symbol = symb # int( symb ) if symb.isdigit( ) else // Doing it elsewhere? watch for bugs
		if theType != SCompiler.LINE :
			SCompiler.prepDataLocation( self )
			self.symbolTable[ symInd ].location = self.dataCounter
			if theType == SCompiler.CONST :
				self.smlData[ self.dataCounter ] = int( symb )
			# variables are already initialized to 0 & updated by let or input.
		else : # line
			self.symbolTable[ symInd ].location = self.instructionCounter
		return symInd

	def getType( self, unknown ) :
		'Only for var & const. Instances of line numbers are invariant'
		if unknown.isdigit( ) :
			return SCompiler.CONST
		else :
			return SCompiler.VAR
			
	def comment( self, restOfLine ) :
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

	def finished( self, restOfLine ) :
		"# halt"
		self.smlData[ self.instructionCounter ] = SCompiler.HALT

	def userInput( self, restOfLine ) :
		"# input x (meaning) store input in var x"
		if restOfLine[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Simple will not use numbers (" + restOfLine[ 0 ] + ") as variable names" )
		whereInd = SCompiler.getSymbolIndex( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		self.smlData[ self.instructionCounter ] = SCompiler.READ + self.symbolTable[ whereInd ].location

	def saveNonLine( self, symbol ) :
		'returns symbolTable index of saved for consts & vars'
		symType = SCompiler.getType( self, symbol )
		if symType == SCompiler.CONST :
			index = SCompiler.getSymbolIndex( self, int( symbol ), symType, SCompiler.RESERVE )
		else :
			index = SCompiler.getSymbolIndex( self, symbol, symType, SCompiler.RESERVE )
		return index

	def screenOutput( self, restOfLine ) :
		"# print x" # or a number, if you are silly
		whereInd = SCompiler.saveNonLine( self, restOfLine[ 0 ] )
		self.smlData[ self.instructionCounter ] = SCompiler.WRITE + self.symbolTable[ whereInd ].location

	def goto( self, opType, lineNumIndex, lineNumDefined, numIfNot ) :
		'emit goto in smlData or do naive to 0 & flag for resolution on second pass'
		if lineNumDefined :
			self.smlData[ self.instructionCounter ] = opType + self.symbolTable[ lineNumIndex ].location
		else :
			# flag for later substitution
			self.lineFlags[ self.instructionCounter ] = int( numIfNot ) # can't look in sTab, not reserved
			# write a tentative goto
			self.smlData[ self.instructionCounter ] = opType # points at 3X00

	def symbFound( self, index ) :
		'ie a line number is in this index of lineFlags'
		return index >= 0

	def branch( self, restOfLine ) :
		"#1 goto #2"
		lineTarget = restOfLine[ 0 ]
		if not lineTarget.isdigit( ) :
			SCompiler.syntaxError( self, "can't jump to variable " + lineTarget + ", only to int line numbers" )
		whereIndex = SCompiler.getSymbolIndex( self, lineTarget, SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.BRANCH, whereIndex, \
				SCompiler.symbFound( self, whereIndex ), lineTarget )

	def simulateOrEquals( self ) : # fix
		'subtract one more to push an equals to neg'
		# given x>y, y-x < 0; if I want x>=y then y-x may = 0
		## CUT THIS, substitute subtracting one from limit
		indOfOne = SCompiler.getSymbolIndex( self, 1, SCompiler.CONST, SCompiler.RESERVE )
		SCompiler.prepInstruction( self )
		self.smlData[ self.instructionCounter ] = SCompiler.SUBTRACT + self.symbolTable[ indOfOne ].location

	def conditionalProduction( self, firstInd, secondInd, orEqual ) :
		'loads first, subtracts second; IF orEqualTo subtracts one more, so GO_NEG works'
		# save: load first to acc
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + \
				self.symbolTable[ firstInd ].location
		# save: subtract second from first
		SCompiler.prepInstruction( self )
		self.smlData[ self.instructionCounter ] = SCompiler.SUBTRACT + \
				self.symbolTable[ secondInd ].location
		if orEqual :
			SCompiler.simulateOrEquals( self )

	def validateIfgotoExpression( self, expression ) :
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

	def relationConditional( self, whereX, whereY, comparison, lineNumSymb ) :
		'uses GO_NEG rather than zero; comparison fsm ensures sensible subtractions'
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
		whereLine = SCompiler.getSymbolIndex( self, lineNumSymb, SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.prepInstruction( self )
		SCompiler.goto( self, SCompiler.BRANCHNEG, whereLine, SCompiler.symbFound( self, whereLine ), lineNumSymb )
	
	def equalityConditional( self, whereX, whereY, comparison, lineNumSymb ) :
		SCompiler.conditionalProduction( self, whereX, whereY, False ) # not orEquals
		whereLine = SCompiler.getSymbolIndex( self, lineNumSymb, SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.prepInstruction( self )
		SCompiler.goto( self, SCompiler.BRANCHZERO, whereLine, SCompiler.symbFound( self, whereLine ), lineNumSymb )
	
	def conditional( self, restOfLine ) :
		"# if x > y goto #2"
		SCompiler.validateIfgotoExpression( self, restOfLine )
		whereX = SCompiler.saveNonLine( self, restOfLine[ 0 ] )
		comparison = restOfLine[ 1 ]
		whereY = SCompiler.saveNonLine( self, restOfLine[ 2 ] )
		target = restOfLine[ 4 ]
		# resolve conditional expression
		if comparison == "==" :
			SCompiler.equalityConditional( self, whereX, whereY, comparison, target )
		else :
			SCompiler.relationConditional( self, whereX, whereY, comparison, target )

	def checkFirstTwoChars( self, varNequal ) :
		if varNequal[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Can't assign new values to numbers" )
		# also, don't assign to lengths.
		elif varNequal[ 1 ] is not "=" :
			SCompiler.syntaxError( self, "Expected '=' after assignment target " + varNequal[ 0 ] )
	
	def isOperator( self, char ) :
		return char in SCompiler.operators
		
	def checkForUnexpected( self, expression ) : # refactor to less magic numbers
		'realistically, I should determine the alternating nature of the expression. Later'
		# ( ( ( x - 5 / x ) + z ) ) - a
		# # pair parenthises => x - 5 / x + z - a ; check alternating alnum operator
		# I'll figure out something eventually
		#
		for ex in expression :
			if ex.isalnum( ) :
				continue
			elif SCompiler.isOperator( self, ex ) :
				continue
			else :
				SCompiler.syntaxError( self, "Invalid symbol in expression " + ex )
		
	def checkDenominator( self, whereDenominator ) :
		"unreliable check if denom = 0; loops through symTab looking for location"
		"""
		In fact, there is no way (halting problem) that I can check at compile time whether
		the denominator is surely 0 without evaluating the program. A const denominator is
		safe, but any variable is initialized to 0. I would have to keep track of variables
		changed in let or input statements ( & input could be zero again ) and flag any that weren't.
		"""
		ind = 0
		limit = self.currSym
		while ind <= limit :
			if self.symbolTable[ ind ].location == whereDenominator : # how much overlap is possible?
				if self.symbolTable[ ind ].type == SCompiler.CONST :
					if self.symbolTable[ ind ].symbol != 0 :
						return # safe denominator
					else :
						#print self.symbolTable[ ind ].symbol
						SCompiler.syntaxError( self, "You put a zero as a denominator" ) 
				else : # is a variable
					# compromise since it could be anything.
					print "Warning: potential zero denominator at line %d" % self.lastLine
					return
			ind += 1
	
	def orderSensitive( self, mathOperator ) :
		return mathOperator != '+' and mathOperator != '*' and mathOperator != '>'

	def saveVal( self, symb, type ) :
		symIndex = SCompiler.getSymbolIndex( self, symb, type, SCompiler.RESERVE )
		whereMem = self.symbolTable[ symIndex ].location
		return whereMem

	def saveTempVal( self ) :
		SCompiler.prepDataLocation( self )
		return self.dataCounter
		
	def loadInAcc( self, memLocation ) :
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + memLocation
		SCompiler.prepInstruction( self )
	
	def storeAcc( self ) :
		# weird to move around information that my future self generates
		memLocation = SCompiler.saveTempVal( self )
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + memLocation
		SCompiler.prepInstruction( self )
		return memLocation

	def performOperation( self, opCode, memLocation ) :
		self.smlData[ self.instructionCounter ] = opCode + memLocation
		SCompiler.prepInstruction( self )

	def applyOperation( self, operator, memLocation ) :
		if '+' == operator :
			SCompiler. performOperation( self, SCompiler.ADD, memLocation )
		elif '-' == operator :
			SCompiler. performOperation( self, SCompiler.SUBTRACT, memLocation )
		elif '*' == operator :
			SCompiler. performOperation( self, SCompiler.MULTIPLY, memLocation )
		elif '/' == operator :
			#SCompiler.checkDenominator( self, memLocation ) # um, not always?
			# sin, I hate to not check but this just became past my available time to resolve
			# make sure that this is checking the denominator
			# because it said n = 5 * y - 0 / x is a const in the denominator
			## problem, this IS treating 0 as the denominator, am I applying it backwards?
			SCompiler. performOperation( self, SCompiler.DIVIDE, memLocation )
		elif '%' == operator :
			SCompiler. performOperation( self, SCompiler.MODULUS, memLocation )
		else :
			pass # assert: unreachable

	def resolveAcc( self, stack, next, afterNext ) :
		'Optimization: do I store or leave value in acc? returns firstValStored'
		saveOver = True
		if SCompiler.isOperator( self, next ) : ## ? x 5 + _
			if SCompiler.orderSensitive( self, next ) : ## 5 x 5 + /
				saveOver = True
				memLocation = SCompiler.storeAcc( self )
				stack.push( memLocation ) # garbage collect as next optimization
			else :								## ? x 5 + +
				saveOver = False # mixing metaphores here as first is actually stored
		elif SCompiler.isOperator( self, afterNext ) : # ? x 5 + ? _
			if SCompiler.orderSensitive( self, afterNext ) :
				saveOver = True
				memLocation = SCompiler.storeAcc( self ) ## 5 x 5 + /
				stack.push( memLocation )
			else :								## ? x 5 + ? *
				saveOver = False # save next, then apply
		else : # ? x 5 + ? x ; these are separate expressions, joined later
			saveOver = False
			memLocation = SCompiler.storeAcc( self )
			stack.push( memLocation )
			# sin, will tempVals retain the change? I forget. python.
		return saveOver
	
	def evaluatePostFix( self, postfix ) : # fixing from pseudo
		'convert polish equation to SML instructions & mem reservations '
		tempVals = stack.Stack( )
		eqInd = 0
		x = 0
		y = 0
		peek = 0
		memLocation = 0
		firstValStored = False # only applies to explicit vals, not temps
		postfix.append( ">" ) # sentinel
		focus = postfix[ eqInd ]
		while '>' != focus :
			if not SCompiler.isOperator( self, focus ) :
				if focus.isdigit( ) :
					memLocation = SCompiler.saveVal( self, int( focus ), SCompiler.CONST )
				elif focus.isalpha( ) :
					memLocation = SCompiler.saveVal( self, focus, SCompiler.VAR )
				# else handle an array lookup aRR[x] or array Length: aRR.len or str.len
				if not firstValStored :
					tempVals.push( memLocation )
					firstValStored = True
				else :
					SCompiler.loadInAcc( self, memLocation )
			else : # operator
				memLocation = tempVals.pop()
				SCompiler.applyOperation( self, focus, memLocation )
				if eqInd + 2 == postfix.__len__( ) : # ie next is sentinel
					break
				else :
					firstValStored = SCompiler.resolveAcc( self, \
					tempVals, postfix[ eqInd + 1 ], postfix[ eqInd + 2 ] )
			# does firstValStored stand up to multiple expressions? 5 8 6 4 + + +
			# or is that invalid polish notation? It's been too long since I made postfixer
			# so I'm probably overspecifying that optimization
			eqInd += 1
			focus = postfix[ eqInd ]

	def assignment( self, restOfLine ) :
		'form of let x = ( y + 2 ) / 99 * z'
		SCompiler.checkFirstTwoChars( self, restOfLine[ :2 ] ) # x =
		# that's not consistent slicing syntax, Guido
		print restOfLine
		SCompiler.checkForUnexpected( self, restOfLine[ 2: ] )
		indexFinal = SCompiler.getSymbolIndex( self, restOfLine[ 0 ], \
			SCompiler.VAR, SCompiler.RESERVE )
		# convert the rest via shunting yard
		decrypted = postFixer.convertToPostFix( restOfLine[ 2: ], False )
		SCompiler.evaluatePostFix( self, decrypted )
		# answer left in the acc, store into x
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + \
			self.symbolTable[ indexFinal ].location

	def saveThisLinesNumber( self, lineNumber ) :
		'save the line number in symbolTable; since increasing, dont search'
		if not lineNumber.isdigit( ) :
			SCompiler.syntaxError( self, "First symbol must be a line number" )
		SCompiler.checkLineNumbersIncreasing( self, int( lineNumber ) )
		SCompiler.getSymbolIndex( self, int( lineNumber ), SCompiler.LINE, SCompiler.RESERVE ) # just reserving
	
	def firstPass( self, line ) :
		'validate/prep lineNum, prep next Instruction, call command( )'
		segment = line.split( ' ' )
		lineNumber = segment[ 0 ]
		comm = segment[ 1 ]
		SCompiler.validateCommandType( self, comm )
		SCompiler.prepInstruction( self )
		SCompiler.saveThisLinesNumber( self, lineNumber )
		newInstruc = SCompiler.commandList[ comm ] # string of the function name
		newInstruc( self, segment[ 2: ] ) # cut line number & command, send restOfLine

	def syntaxErrorSecondPass( self, why ) :
		'just for resolving forward referenced lines'
		print "\nXX\nXX > Error, " + why + "\nXX"
		SCompiler.showState( self )
		if SCompiler.TESTING :
			SCompiler.FAILED = True
		else :
			exit( 1 )

	def resolveForwardReferencedLines( self ) :
		'lineFlags are initialized to -1; forward references contain lineNumber (ie symbol) pointed at'
		# Resolves self.lineFlags[ self.instructionCounter ] = int( self.symbolTable[ lineNumIndex ].symbol ) from goto()
		ind = 0
		limit = self.lineFlags.__len__( )
		while ind < limit :
			lineNum = self.lineFlags[ ind ]
			if lineNum >= 0 :
				# find that line number in symbolTable
				whereInd = SCompiler.getSymbolIndex( self, lineNum, SCompiler.LINE, not SCompiler.RESERVE )
				# resolve
				if not SCompiler.symbFound( self, whereInd ) :
					SCompiler.syntaxErrorSecondPass( self, "referenced line number " + \
						str( lineNum ) +" for instruction " + str( ind ) + " not found" )
				else :
					self.smlData[ ind ] += self.symbolTable[ whereInd ].location # was 4100, now 41xx
			ind += 1

	def saveProgram( self, originalFileName ) :
		'write to filename.sml # return that name'
		newFileName = originalFileName[ : -3 ] + "sml" # replaces .txt or similar
		output = open( newFileName, 'w' )
		output.truncate( ) # erase what's in there for safety
		for nn in self.smlData :
			output.write( str( nn ) + '\n' ) # consider using same technique as Ram.coreDump
		output.close( )
		return newFileName

	def secondPass( self, originalFileName ) :
		'resolve goto statements, print to x.sml return that filename'
		SCompiler.showState( self )
		SCompiler.resolveForwardReferencedLines( self )
		return SCompiler.saveProgram( self, originalFileName )

	def compile( self, simpleFile ) :
		'compiles or reports syntaxError, returns name of new sml file to run'
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
	operators = [ "/", "*", "+", "-", "%", ">", '(', ')' ]
	# added sentinel to guard against array overflow during optimization

'''	OUTPUT
        using monkey.txt

        Forward referenced lines:
line called 9 referenced by instruction in mem 3
line called 10 referenced by instruction in mem 6

        Contents of Symbol Table        index - 15
 sym     type    location
 1       line num        0
 2       line num        0
 3       line num        0
 5       const num       29
 6       line num        1
 x       variable        28
 7       line num        2
 9       line num        4
 3       const num       27
 1       const num       26
 10      line num        7
 5       const num       25
 11      line num        9
 y       variable        24
 6       const num       23
 53      line num        14

Instr count - 14        Data counter - 22
        Contents of sml data bank
        0       1       2       3       4
        1129    1028    0000    3000    4027
5       2126    3100    4025    4128    4023
10      2025    4122    4022    4124    0000
15      0000    0000    0000    0000    0000
20      0000    0000    0000    0006    0000
25      0005    0001    0003    0000    0005    done
paused so you can fix monkey.sml so it looks at 3 instead of 2d
	[simpletron output]
 print to terminal:  5
 wait for terminal input
 -- 4
 print... // changed this during pause, used to be "0"
 naive goto ptr to 4
 load Acc with 3 from 27
 subtract (acc) 3 and 1
 if Acc (2) is zero, goto 7
 load Acc with 5 from 25
 save acc, 5, into 28
 load Acc with 6 from 23
 add (acc) 6 and 5
 save acc, 11, into 22
 load Acc with 11 from 22
 save acc, 11, into 24
 Halt program

[monkey prettified]
 0 print from 29
 1 input to 28
 2 ..0
 3 goto 4
 4 load acc from 27
 5 - - acc & from 26
 6 if acc Negative goto 7
 7 load acc from 25
 8 store acc into 28
 9 load acc from 23
 10 ++ acc & from 25
 11 store acc into 22
 12 load acc from 22
 13 store acc into 24

[monkey in simple]
 1 rem monkey wrench program, not designed to be run on simpletron
 2 rem
 3 print 5
 6 input x
 7 goto 9
 9 if 3 == 1 goto 10
 10 let x = 5
 11 let y = 6 + 5
 53 end
'''