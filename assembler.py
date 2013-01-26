'''	Hand Eller:
source
output
hw assessment
	goal: both 2 & 3 compliance

	FINISHED
initial pass: op var name

	DOING
initial pass: var val?comm?

	NEED
print code
test driver
second pass, resolve forward reference, save file
(verbose?)
'''

class Assembler( object ) :
	'converts either a file or list of sml assembly to sml op codes'

	def __init__( self ) :
		self.op_spot = 0
		self.var_spot = 1
		self.name_spot = 2
		self.lines_done = 0
		self.output = [] # stores tuples or lists temporarily
		self.ref_flags = []
		self.symbols = {} # dict
	
	def assemble_file( self, asm_file, auto_mode ) : #, verbose_mode ) :
		'changes sml asm file into simpletron instructions in nn.asm'
		try :
			asm_program = open( asm_file ) # py 3 compliant?
			for line in asm_program :
				lines_done += 1
				input = line.rstrip( '\n' )
				self.initial_pass( input.split( ' ' ) )
			asm_program.close()
		except IOError :
			print "File Error: Perhaps an invalid name?" # 2to3
		if auto_mode :
			new_file = self.cleanup_pass_f( asm_file )
			return new_file
		else :
			self.cleanup_pass( asm_file )

	def assemble_stream( self, asm_list ) :
		'receive a list of asm strings, perhaps from test'
		for line in asm_list :
			lines_done += 1
			self.initial_pass( line.split( ' ' ) )
		self.cleanup_pass( None )

	def is_a_comment( self, char ) :
		return char == '#'

	def save_outp( self, pair ) :
		'saves pair, side effect: returns index of pair'
		output.append( pair )
		return output.__len__() - 1

	def to_num_flag( self, in_var ) :
		'if string is numbers, cast; report whether it did'
		if in_var.isdigit() :
			return int( in_var ), True
		else :
			return in_var, False

	def save_var_with_op( op_word, ok_var ) : # deeply consider what's saved
		'if var already saved, put with op_word in tuple, else save ref_flag'
		if ok_var not in symbols :
			out_index = save_outp( [ op_word, ok_var ] )
			ref_flags.append( [ ok_var, out_index ] )
			# then val_line = symb[ ref[ nn[0] ] ]
			# output[ ref[ nn[1] ] ][var_spot] = output[ val_line ][var_spot] or val line? sin
		else :
			out_index = save_outp( (op_word, symbols[ ok_var ]) ) #tuple, outp_ind of value
		return out_index # in case line has a name

	def save_op_line( self, input, in_op ) :
		ok_var = self.to_num_flag( input[ var_spot ] )
		line_index = self.save_var_with_op( asm_sml[ in_op ], ok_var )
		# handle line name/comment
		if input.__len__( ) > var_spot + 1 : # has another token
			in_name = input[ name_spot ]
			if not self.is_a_comment( in_name[ 0 ] ) :
				symbols[ in_name ] = line_index
'''
	output.append( ( key_words[ 'no_op' ], const ) )
	symbols[ const ] = output_index
'''

	def save_const_line( self var_value ) :
		'line was: 5 ; discard remaining'
		# this form correct for vars
		output_index = self.save_outp( ('no_op', var_value) )
		symbols[ var_value ] = output_index

	def save_variable_line( self, variable ) : # deeply consider what's saved
		'potentially: x // x 5 // x y ; discard remaining'
		# actually that variable assignment could be a problem?
		# or is second pass enough as they will both default to 0?
		maybe_val = input[ var_spot ]
		if is_a_comment( maybe_val[0] ) :
			var_value = 0
		elif maybe_val.isdigit() :
			var_value = int( maybe_val )
		elif maybe_val in symbols :
			val_index = symbols[ maybe_val ]
			var_value = output[ val_index ][var_spot] # might be wrong
			line_index = self.save_outp( ('no_op', var_value) )
			symbols[ maybe_val ] = line_index
		else :
			raise TypeError('unknown val for var on line ' + str(lines_done))

	def save_var_line( self, input, in_var ) :
		var_value, is_num = to_num_flag( in_var )
		if is_num and var_value not in symbols :
			self.save_const_line( var_value )
		else :
			self.save_variable_line()

	#if var found, save mem index; else save symb for searching ref_flags later
	def initial_pass( self, input ) :
		'receive either (op var [line name]), var, or #comment'
		in_op = input[ op_spot ]
		if self.is_a_comment( in_op[ 0 ] ) : # whole line
			return
		elif in_op in asm_sml :
			self.save_op_line( input, in_op )
		else : # is a data allocation
			self.save_var_line( input, in_op )

'''
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
	def cleanup_pass( self, file_name_maybe ) :
		'resolve forward references, emit sml appropriately'
		# cleanup forward references
		# export somehow
		if file_name_maybe is not None :
			self.save_file( file_name_maybe )
		print 'cleanup pass is an empty method'
		







	
	
	
	
	
	
	
	
	asm_sml : {
		'READ' : 1000,
		'WRITE' : 1100,
		'LOAD' : 2000,
		'STORE' : 2100,
		'ADD_' : 3000,
		'MINUS' : 3100,
		'DIVIDE' : 3200,
		'TIMES' : 3300,
		'MODUL' : 3400,
		'GONOW' : 4000,
		'GOIF-' : 4100,
		'GOIF0' : 4200,
		'HALT' : 4300,
		'no_op' : 0 }
