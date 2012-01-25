
# Nicholas Prado
# Might as well practice testing

import compiler

def test_syntaxError( compiler ) :
	# syntaxError( self, why ) :
	compiler.syntaxError( "testing errors" )

def test_validateCommandType( compiler ) :
	# checkLineNumbersIncreasing( self, newLineNumber ) :
	pass

def test_searchForSymbol( compiler ) :
	compiler.searchForSymbol( "x" )

def test_programTooBig( compiler ) :
	pass

def test_reserveNewSymbol( compiler ) :
	pass

def test_comment( compiler ) :
	pass

def test_finished( compiler ) :
	pass

def test_userInput( compiler ) :
	pass

def test_screenOutput( compiler ) :
	pass

def test_branch( compiler ) :
	pass

def test_conditional( compiler ) : 
	pass

def test_assignment( compiler ) :
	pass

tool = compiler.SCompiler( )
test_validateCommandType( tool )
test_searchForSymbol( tool )
test_programTooBig( tool )
test_reserveNewSymbol( tool )
test_comment( tool )
test_finished( tool )
test_userInput( tool )
test_screenOutput( tool )
test_branch( tool )
test_conditional( tool )
test_assignment( tool )
test_syntaxError( tool )
'''
	# validateCommandType( self, word ) :
	# searchForSymbol( self, sought, typeSought )
	# def programTooBig( self ) :
	# def reserveNewSymbol( self, symb, theType )
	# def comment( self, restOfLine )
	# def finished( self, restOfLine )
	# def userInput( self, restOfLine )
	# def screenOutput( self, restOfLine ) :
	# def branch( self, restOfLine ) :
	# def conditional( self, restOfLine ) : 
	# def assignment( self, restOfLine ) :
	# def firstPass( self, line ) :
	# def resolveForwardReferencedLines( self ) :
	# def saveProgram( self ) :
	# def secondPass( self ) :
'''