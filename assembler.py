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
	
	def __str__( self ) :
		return str( self.op_type ) + ' : ' + str( self.operand )

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
		self.asm_sml = {
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
			self.lines_done += 1
			self.initial_pass( line.split( ' ' ) )
		self.cleanup_refs( )
		return self.become_code() # list[] of sml ops as ints

	def is_a_comment( self, char ) :
		return char == '#'

	def save_outp( self, op_n, ind_addr ) : # vetted
		'saves pair, side effect: returns index of pair'
		pair = Instruction( op_n, ind_addr )
		self.output.append( pair )
		return self.output.__len__() - 1

	def to_num_flag( self, in_var ) :
		'if string is numbers, cast; report whether it did'
		if self.is_a_comment( in_var[0] ) :
			raise TypeError('no operand for instruction on line ' + str(lines_done))
			# oh, but what about- I was going to say READ, but it's ram direct. hmm
			# check the spec.
		elif in_var.isdigit() :
			return int( in_var ), True
		else :
			return in_var, False

	def save_var_with_op( self, op_word, ok_var ) : # okay
		'if var already saved, put in new Instruction, else save ref_flag'
		out_index = -1 # init outside of branch, le sigh
		if ok_var in self.symbols :
			out_index = self.save_outp( op_word, self.symbols[ ok_var ] )
		else :
			out_index = self.save_outp( op_word, ok_var )
			self.ref_flags.append( out_index )
		return out_index # in case line has a name

	def save_op_line( self, input, in_op ) : # okay
		ok_var, discard_flag = self.to_num_flag( input[ self.var_spot ] ) # flag irrelevant
		line_index = self.save_var_with_op( self.asm_sml[ in_op ], ok_var )
		# handle line name/comment
		if input.__len__( ) > self.var_spot + 1 : # has another token, maybe line name
			in_name = input[ self.name_spot ]
			if not self.is_a_comment( in_name[ 0 ] ) :
				self.symbols[ in_name ] = line_index

	def save_const_line( self, var_value ) : # vetted
		'line was: "5" ; discard remaining'
		# this form correct for vars
		output_index = self.save_outp(  self.asm_sml[ 'no_op' ], var_value )
		self.symbols[ var_value ] = output_index

	def s_v_l_determine_value( self, maybe_value ) :
		'finds value or gives default, else temp mark in ref_flags'
		if maybe_value.isdigit() :
			return int( maybe_value )
		elif maybe_value in self.symbols :
			return self.output[ self.symbols[maybe_value] ].operand
		elif not self.is_a_comment( maybe_value[0] ) : # ? var case, ie forward referenced
			self.ref_flags.append( variable ) # hack to signal s_v_line() to fix with real ind
			return 0
		else : # is a comment
			return 0
				
	def save_variable_line( self, remaining, variable ) : # looks okay
		'potentially: x // x 5 // x y ; discard remaining'
		var_value = 0 # default for variables
		if len( remaining ) > self.var_spot : # comment or AoT assignment
			var_value = self.s_v_l_determine_value( remaining[ self.var_spot ] )
		ref_ind = self.save_outp(  self.asm_sml[ 'no_op' ], var_value )
		self.symbols[ variable ] = ref_ind
		if len( self.ref_flags ) > 0 and self.ref_flags[ -1 ] == variable :
			# newest is the ? var case in s_v_l_d_v()
			self.ref_flags[ -1 ] = ref_ind

	def save_var_line( self, input, in_var ) : # okay
		var_value, is_num = self.to_num_flag( in_var )
		if is_num :
			if var_value not in self.symbols :
				self.save_const_line( var_value )
		else :
			self.save_variable_line( input, in_var )

	#if var found, save mem index; else save symb for searching ref_flags later
	def initial_pass( self, input ) :
		'receive either (op var [line name]), var, or #comment'
		first_token = input[ self.op_spot ]
		if self.is_a_comment( first_token[ 0 ] ) : # whole line
			return
		elif first_token in self.asm_sml :
			self.save_op_line( input, first_token )
		else : # is a data allocation
			self.save_var_line( input, first_token )

	def cleanup_refs( self ) :
		'resolve forward references, emit sml appropriately'
		for problem in self.ref_flags :
			wanted_symbol = self.output[ problem ].operand
			if wanted_symbol in self.symbols :
				self.output[ problem ].operand = self.symbols[ wanted_symbol ]
			else :
				raise ValueError('unreserved val for op on line ' + str(problem) \
					+ " " + str(wanted_symbol) )
		# do I need to resolve recursive references?

	def become_code( self ) :
		sml = []
		for pair in self.output :
			sml.append( pair.op_type + pair.operand )
		return sml
	
	def index_of_period( file_name ) :
		for back_ind in range( -1, -6, -1 ) : # 2to3 ? # sort of arbitrary
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

	def t_clear( self ) :
		self.symbols = {}
		self.ref_flags = []
		self.output = []

def test_good_syn( simple ) :
	asm = [ "x", "y 5", "z y", '5', "aa #comment", \
		"# comment", "#comment", \
		'MODUL 5', 'GONOW bla', 'GOIF- up bla', \
		'READ up up #hmm will it blend?' ]
	should_be = [ 0, 5, 5, 5, 0, 3403, \
			4007, 4108, 1008 ]
	became = simple.assemble_stream( asm )
	worked = True
	for ind in range( len( became ) - 1 ) : # 2to3
		if became[ind] != should_be[ind] :
			print " Didnt match on line " + str(ind) \
				+ ", bec-" + str(became[ind]) \
				+ " should-" + str(should_be[ind])# 2to3
			worked = False
	if worked :
		print "good syntax vetted, for now"

def test_bad_syn( simple ) :
	'''
	x x # hmm?
	HALT #unary unfortunately
	TIMES not_init
	y TIMES #maybe?
	'''
	print "doesnt test wrong syntax" # 2to3

def test_syntax( simple ) :
	test_bad_syn( simple )
	simple.t_clear()
	test_good_syn( simple )

def test_assembler() :
	simple = Assembler()
	test_syntax(simple)
	
test_assembler()









