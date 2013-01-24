'''
	goal: both 2 & 3 compliance
verbose mode?
save file name
open file
hand lines to assembler
for entry
	tokenize
	op_maybe = line[ 0 ]
	var_maybe = line[ 1 ]
	if op_maybe in key_words
		if var_maybe in symbols :
			output.append( ( key_words[ op_maybe ], symbols[ ref ] ) )
		else :
			if ref.isnum() :
				ref = int( ref )
			output.append( [ key_words[ op ], ref ] )
			line_flags.append( [ref, output_index )
		if len( line ) > 2 and line[ name ].charAt( 0 ) != '#'
			symbols[ line[ name ] ] = output_index
	elif op_maybe.charAt( 0 ) != '#' :
		if var_maybe.isnum() :
			const = int( var_maybe )
			if const not in symbols :
				output.append( ( key_words[ 'no_op' ], const ) )
				symbols[ const ] = output_index
			# else its already saved
		else : # its a variable
			if var_maybe not in symbols :
				output.append( ( key_words[ 'no_op' ], var_maybe ) )
				symbols[ var_maybe ] = output_index
	# else, it's a comment
close file
if len( line_flags > 0 ) :
	for ref in line_flags :
		missing_symb = ref[ 0 ]
		where_from = ref[ 1 ]
		if missing_symb not in symbols :
			raise TypeError('argument must be an integer') # or whatever
		else :
			output[ where_from ] = ( output[ where_from ][0], symbols[ missing_symb ] )

create file + '.asm'
for instruction in output :
	write( instruction[ 0 ] + instruction [ 1 ] )
close file
report success?
'''

class Assembler( object ) :
	
	def assemble_file( self, asm_file, auto_mode ) : #, verbose_mode ) :
		'changes sml asm file into simpletron instructions in nn.asm'
		try :
			asm_program = open( asm_file )
			for line in asm_program :
				self.initial_pass( line.rstrip( '\n' ) )
			asm_program.close()
		except IOError :
			print "Error: file. Perhaps in invalid name?"
			# print( "Error: file. Perhaps in invalid name?" )
		if auto_mode :
			new_file = self.cleanup_pass_f( asm_file )
			return new_file
		else :
			self.cleanup_pass( asm_file )

	def assemble_stream( self, asm_list ) :
		for line in asm_list :
			self.initial_pass( line )
		self.cleanup_pass_s( )
		
		







	
	
	
	
	
	
	
	
	key_words : {
		'READ' : 1000,
		'WRITE' : 1100,
		'LOAD' : 2000,
		'STORE' : 2100,
		'ADD_' : 3000,
		'MINUS' : 3100,
		'DIVIDE' : 3200,
		'TIMES' : 3300,
		'MODUL' : 3400,
		'GOTO' : 4000,
		'GOIF-' : 4100,
		'GOIF0' : 4200,
		'HALT' : 4300,
		'no_op' : 0 }
