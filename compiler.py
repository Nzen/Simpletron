
# Nicholas Prado
# begun 12 1 11
# Compiler/assembler for Deitel's Simple language into SML for the Simpletron

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

import postFixer
import stack

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

	def __init__( self ) :
		self.symbolTable = [ TableEntry( ) for i in range( SCompiler.RAMSIZE ) ]
		# consider appending to symbol table rather than using an index?
		self.lineFlags = [ -1 ] * SCompiler.RAMSIZE # notes which fail, only because of spec else I'd use a list
		self.smlData = [ 0 ] * SCompiler.RAMSIZE # floods ram later 	// ^ may do anyway, later
		self.instructionCounter = -1
		self.dataCounter = SCompiler.RAMSIZE # sc.RS - 1? 12 3 18
		self.currSym = -1 # index in symbol table of latest
		self.lastLine = -1 # for checkLineNumIncreasing

	def showSymbolTable( self ) :
		print "\n\tContents of Symbol Table\tindex - " + str( self.currSym )
		print "sym\ttype\tlocation"
		ind = 0
		limit = self.currSym #self.symbolTable.__len__( )
		while ( ind <= limit ) :
			print self.symbolTable[ ind ]

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
		#if self.instructionCounter > 1 :
		#	SCompiler.showSymbolTable( self )
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
		self.smlData[ self.instructionCounter ] = SCompiler.STOP

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

	def goto( self, opType, lineNumIndex, lineNumDefined, numIfX ) :
		'emit goto in smlData or do naive to 0 & flag for resolution on second pass'
		SCompiler.prepInstruction( self ) # conditionals seem to prep themselves
		if lineNumDefined :
			self.smlData[ self.instructionCounter ] = opType + self.symbolTable[ lineNumIndex ].location
		else :
			# flag for later substitution
			self.lineFlags[ self.instructionCounter ] = int( numIfX ) # can't look in sTab, not reserved
			# write tentative goto
			self.smlData[ self.instructionCounter ] = opType # points at 3X00

	def symbFound( self, index ) :
		'ie a line number is in this index of lineFlags'
		return index >= 0

	def branch( self, restOfLine ) :
		"#1 goto #2"
		lineTarget = restOfLine[ 0 ]
		if not lineTarget.isdigit( ) :	# POINTS AT Index or resolving is failing
			SCompiler.syntaxError( self, "can't jump to variable " + lineTarget + ", only to int line numbers" )
		# search symbolTable for the referenced line number
		whereIndex = SCompiler.getSymbolIndex( self, lineTarget, SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTO, whereIndex, SCompiler.symbFound( self, whereIndex ), lineTarget )

	def simulateOrEquals( self ) :
		'subtract one more to push an equals to neg'
		# given x>y, y-x < 0; if I want x>=y then y-x may = 0
		indOfOne = SCompiler.getSymbolIndex( self, 1, SCompiler.CONST, SCompiler.RESERVE )
		SCompiler.prepInstruction( self )
		self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ indOfOne ].location

	def conditionalProduction( self, firstInd, secondInd, orEqual ) :
			'loads first, subtracts second; IF orEqualTo subtracts one more, so gotoNeg works'
			# save: load first to acc
			self.smlData[ self.instructionCounter ] = SCompiler.LOAD + self.symbolTable[ firstInd ].location
			# save: subtract second from first
			SCompiler.prepInstruction( self )
			self.smlData[ self.instructionCounter ] = SCompiler.SUBTR + self.symbolTable[ secondInd ].location
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
		'uses gotoNeg rather than zero; comparison fsm ensures sensible subtractions' # what the hell?
		orEquals = True
		if comparison == ">=" :
			SCompiler.conditionalProduction( self, whereY, whereX, orEquals ) # so many uninitialized?
		elif comparison == "<=" :
			SCompiler.conditionalProduction( self, whereX, whereY, orEquals )
		elif comparison == ">" :
			SCompiler.conditionalProduction( self, whereY, whereX, not orEquals )
		else : # must be "<"
			SCompiler.conditionalProduction( self, whereX, whereY, not orEquals )
		# resolve goto
		whereLine = SCompiler.getSymbolIndex( self, restOfLine[ 4 ], SCompiler.LINE, not SCompiler.RESERVE )
		SCompiler.goto( self, SCompiler.GOTONEG, whereLine, SCompiler.symbFound( self, whereLine ), lineNumSymb )
	
	def conditional( self, restOfLine ) :
		"# if x > y goto #2"
		SCompiler.validateIfgotoExpression( self, restOfLine )
		whereX = SCompiler.saveNonLine( self, restOfLine[ 0 ] )
		comparison = restOfLine[ 1 ]
		target = restOfLine[ 4 ]
		whereY = SCompiler.saveNonLine( self, restOfLine[ 2 ] )
		# resolve conditional expression
		if comparison == "==" :
			SCompiler.conditionalProduction( self, whereX, whereY, False ) # not orEquals
			whereLine = SCompiler.getSymbolIndex( self, target, SCompiler.LINE, not SCompiler.RESERVE )
			SCompiler.goto( self, SCompiler.GOTOZERO, whereLine, SCompiler.symbFound( self, whereLine ), target )
		else :
			SCompiler.relationConditional( self, whereX, whereY, comparison, target )

	def checkFirstTwoChars( self, varNequal ) :
		if varNequal[ 0 ].isdigit( ) :
			SCompiler.syntaxError( self, "Can't assign new values to numbers" )
		elif varNequal[ 1 ] is not "=" :
			SCompiler.syntaxError( self, "Expected '=' after assignment target " + varNequal[ 0 ] )
		
	def checkForUnexpected( self, expression ) :
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

	def spotForTempAnswer( self ) :
		SCompiler.prepDataLocation( self )
		return self.dataCounter

	def mathProduction( self, whereY, operator, whereX ) :
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
						SCompiler.syntaxError( self, "You put a zero as a denominator" ) 
				else : # is a variable
					# compromise since it could be anything.
					print "Warning: potential zero denominator at line %d" % self.lastLine
					return
			ind += 1

	def evaluateCode( self, whereY, operator, whereX ) :
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

	def evaluatePostFix( self, postfix ) :
		' convert polish equation to SML instructions & mem reservations '
		tempVals = stack.Stack( )
		ind = 0 # was name conflicting with indecies below
		y = 0
		x = 0
		postfix.append( ">" ) # sentinel
		focus = postfix[ ind ]
		while ">" is not focus :
			if focus.isdigit( ) :
				symIndex = SCompiler.getSymbolIndex( self, focus, SCompiler.CONST, SCompiler.RESERVE )
				where = self.symbolTable[ symIndex ].location
				tempVals.push( where )
			elif focus.isalpha( ) :
				symIndex = SCompiler.getSymbolIndex( self, focus, SCompiler.VAR, SCompiler.RESERVE )
				where = self.symbolTable[ symIndex ].location
				tempVals.push( where )
			else : # isOperator( )
				x = tempVals.pop( )
				y = tempVals.pop( )
				tempLocation = SCompiler.evaluateCode( self, y, focus, x )
				tempVals.push( tempLocation )
			ind += 1
			focus = postfix[ ind ]
		return tempVals.pop( ) # answer location

	def assignment( self, restOfLine ) :
		'form of let x = ( y + 2 ) / 99 * z'
		SCompiler.checkFirstTwoChars( self, restOfLine[ :2 ] ) # that's not consistent slicing syntax, Guido
		SCompiler.checkForUnexpected( self, restOfLine[ 2: ] )
		indexFinal = SCompiler.getSymbolIndex( self, restOfLine[ 0 ], SCompiler.VAR, SCompiler.RESERVE )
		decrypted = postFixer.convertToPostFix( restOfLine[ 2: ], False ) # cut x = ;; convert not verbosely
		penultimateLocation = SCompiler.evaluatePostFix( self, decrypted ) # mixing locations & symTab indexes is weird
		# penultimate into acc
		self.smlData[ self.instructionCounter ] = SCompiler.LOAD + penultimateLocation ## should I make this sort of assignment OO style?
		SCompiler.prepInstruction( self )
		# store into whereFinal
		self.smlData[ self.instructionCounter ] = SCompiler.STORE + self.symbolTable[ indexFinal ].location

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