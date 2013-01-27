'''	Hand Eller:
source
output
hw assessment
	goal: both 2 & 3 compliance

	FINISHED
initial pass: op var name ;; var val?comm?
final pass

	DOING
print code

	NEED
test driver
second pass, resolve forward reference, save file
(verbose?)

raise TypeError('unknown val for var on line ' + str(lines_done))
'''
class Instruction( object ) :
	def __init__( self, operation, ref_addr ) :
		self.op_type = operation
		self.operand = ref_addr
	# put representation limits in here?

class Assembler( object ) :
	'converts either a file or list of sml assembly to sml op codes'

	def __init__( self ) :
		self.op_spot = 0
		self.var_spot = 1 # used outside literal var spot for similar indicies too
		self.name_spot = 2
		self.lines_done = 0 # for errors in initial pass
		self.output = [] # stores Instructions, forward ref gets symb_name
		self.ref_flags = [] # index of Instruction with a forward_reference
		self.symbols = {} # dict; var_name : output_index_of_val

	def get_file_lines_for_initial( self, asm_file ) :
		try :
			asm_program = open( asm_file ) # py 3 compliant?
			for line in asm_program :
				lines_done += 1
				input = line.rstrip( '\n' )
				self.initial_pass( input.split( ' ' ) )
			asm_program.close()
		except IOError :
			print "File Error: Perhaps an invalid name?" # 2to3

	def assemble_file( self, asm_file ) : #, verbose_mode ) :
		'changes sml asm file into simpletron instructions in nn.asm'
		self.get_file_lines_for_initial( asm_file )
		self.cleanup_refs( )
		self.become_code( )
		return self.save_sml_file( self.become_code(), asm_file )

	def assemble_stream( self, asm_list ) :
		'receive a list of asm strings, perhaps from test'
		for line in asm_list :
			lines_done += 1
			self.initial_pass( line.split( ' ' ) )
		self.cleanup_refs( )
		return self.become_code() # list[] of sml ops as ints

	def is_a_comment( self, char ) :
		return char == '#'

	def save_outp( self, op_n, ind_addr ) : # vetted
		'saves pair, side effect: returns index of pair'
		pair = Instruction( op_n, ind_addr )
		output.append( pair )
		return output.__len__() - 1

	def to_num_flag( self, in_var ) :
		'if string is numbers, cast; report whether it did'
		if is_a_comment( in_var[0] ) :
			raise TypeError('no operand for instruction on line ' + str(lines_done))
			# oh, but what about- I was going to say READ, but it's ram direct. hmm
			# check the spec.
		elif in_var.isdigit() :
			return int( in_var ), True
		else :
			return in_var, False

	def save_var_with_op( op_word, ok_var ) : # okay
		'if var already saved, put in new Instruction, else save ref_flag'
		out_index = -1 # init outside of branch, le sigh
		if ok_var in symbols :
			out_index = save_outp( op_word, symbols[ ok_var ] )
		else :
			out_index = save_outp( op_word, ok_var )
			ref_flags.append( [ out_index )
		return out_index # in case line has a name

	def save_op_line( self, input, in_op ) : # okay
		ok_var = self.to_num_flag( input[ var_spot ] ) # flag irrelevant
		line_index = self.save_var_with_op( asm_sml[ in_op ], ok_var )
		# handle line name/comment
		if input.__len__( ) > var_spot + 1 : # has another token, maybe line name
			in_name = input[ name_spot ]
			if not self.is_a_comment( in_name[ 0 ] ) :
				symbols[ in_name ] = line_index

	def save_const_line( self var_value ) : # vetted
		'line was: "5" ; discard remaining'
		# this form correct for vars
		output_index = self.save_outp( 'no_op', var_value )
		symbols[ var_value ] = output_index

	def s_v_l_determine_value( self, maybe_value ) :
		'finds value or gives default, else temp mark in ref_flags'
		if maybe_value.isdigit() :
			return int( maybe_value )
		elif maybe_value in symbols :
			return output[ symbols[maybe_value] ].operand
		elif not is_a_comment( maybe_value[0] ) : # ? var case, ie forward referenced
			ref_flags.append( variable ) # hack to signal s_v_line() to fix with real ind
			return 0
		else : # is a comment
			return 0
				
	def save_variable_line( self, remaining_line, variable ) : # looks okay
		'potentially: x // x 5 // x y ; discard remaining'
		var_value = 0 # default for variables
		if len( remaining ) > var_spot : # comment or AoT assignment
			var_value = self.s_v_l_determine_value( input[ var_spot ] )
		ref_ind = self.save_outp( 'no_op', var_value )
		symbols[ variable ] = ref_ind
		if ref_flags[ -1 ] == variable : # newest is the ? var case in s_v_l_d_v()
			ref_flags[ -1 ] = ref_ind

	def save_var_line( self, input, in_var ) : # okay
		var_value, is_num = to_num_flag( in_var )
		if is_num :
			if var_value not in symbols :
				self.save_const_line( var_value )
		else :
			self.save_variable_line( input, in_var )

	#if var found, save mem index; else save symb for searching ref_flags later
	def initial_pass( self, input ) :
		'receive either (op var [line name]), var, or #comment'
		first_token = input[ op_spot ]
		if self.is_a_comment( first_token[ 0 ] ) : # whole line
			return
		elif first_token in asm_sml :
			self.save_op_line( input, first_token )
		else : # is a data allocation
			self.save_var_line( input, first_token )

	def cleanup_refs( self, file_name_maybe ) :
		'resolve forward references, emit sml appropriately'
		for problem in ref_flags :
			wanted_symbol = output[ problem ].operand
			if wanted_symbol in symbols :
				output[ problem ].operand = symbols[ wanted_symbol ]
			else :
				raise ValueError('unreserved val for op on line ' + str(problem))

	def become_code( self ) :
		sml = []
		for pair in output :
			sml.append( pair.op_type + pair.operand )
		return sml
	
	def index_of_period( file_name ) :
		for back_ind in range( -1, -6, -1 ) # 2to3 ? # sort of arbitrary
			if file_name[ back_ind ] == '.' :
				return back_ind
		else :
			return -4 # whatever

	def save_sml_file( self, sml_code, original_name ) :
		file_type = index_of_period( original_name )
		new_name = original_name[ : file_type ] + '.asm' # hopefully
		output = open( newFileName, 'w' )
		output.truncate( ) # erase what's in there for safety
		for nn in sml_code :
			output.write( str( nn ) + '\n' )
		output.close( )
		return new_name

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












