package sml;

public class Simpletron
{
	private String intro = "*** Welcome to Simpletron! ***\n*** Please enter your program one instruction ***\n*** (or data word) at a time into the input ***\n*** text field. I will display the location ***\n*** number and a question mark (?). You then ***\n*** type the word for that location. Press the ***\n*** Done button to stop entering your program. ***";
	private String endLoad = "*** Program loading completed ***";
	private String beginExe = "*** Program execution begins ***";
	private SmlCpu brain;
	private SmlMem memory;
	private Input stdin;

	public Simpletron( SmlFlag arg )
	{
		if ( arg == SmlFlag.HAND )
		{
			deitelVersion();
		}
		else
		{
			System.out.println( "only deitel version so far" );
		}
	}

	public void deitelVersion( )
	{
		brain = new SmlCpu();
		memory = new SmlMem( 30 );
		stdin = new Input();
		System.out.println( "\n" + intro );
		System.out.println( "\n It actually means put the value -99999 to FINISH" ); // FIX
		System.out.println( "\t" + stdin.getLine() );
		System.out.println( "\n" + endLoad );
		System.out.println( "\n" + beginExe );
	}
	
	/*	some pseudocode
	void execute( instructionVal ){
		signal = cpu.result( instructionVal );
		moveData( signal.path, signal.cargo );
	}

	 	// assuming already indirected
	 	switch( storedInstrAlready ){
	 	 case Instr.INPUT:
	 	 	return new Signal( pair.I_C, instrVal );
	 	 case Instr.STORE:
	 	 	return new Signal( pair.C_R, instrVal );

	void moveData( path, cargo ) {
		switch( path )
		{
		case pair.I_C: {
			brain.receive( stdin.emit( cargo ) );
			break; }
		case pair.S_C: {
			brain.receive( stdout.emit( cargo ) );
			break; }
		case pair.C_C: {
			brain.receive( brain.emit( cargo ) );
			break; }	// it handles distinguishing branch & math

	READ, WRITE, LOAD, STORE
	ADD, SUBTRACT, DIVIDE, MULTIPY, MODULUS, EXPONENT
	BRANCH, BRANCHNEG, BRANCHZERO, HALT
		Rd : inp -> cpu
		Wt : cpu -> out
		Ld : ram -> cpu
		St : cpu -> ram
		+- : cpu -> cpu
		Br : cpu -> cpu
		Hl : cpu -> sml

		[cpu] emit( info ) {
		 switch( info.instr ){
		 case Inst.BRANCH:
		 	return new Ping( info.instr, operand );
		 case Inst.BR_NEG:
		 	if ( acc <= 0 ){
		 		return new Ping( info.instr, operand ) }
		 	else {
		 		return new Ping( info.instr, pc ) }
		 case Inst.ADD:
		 	int temp = acc + operand;
		 	if validSize( temp )
		 		return new Ping( info.instr, temp );
		 	else
		 		throw sizeException;

		 [cpu] receive( Ping instr_result ){
		 	switch( instr_result.opC ){
		 	 case Inst.BRA:
		 	 	pc = instr_result.answ;
		 	 case Inst.ADD:
		 	 	acc = instr_result.answ;
			
	}
	*/
}






