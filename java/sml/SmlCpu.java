package sml;

//package java;

public class SmlCpu
{
	private int acc; // accumulator
	private int pc; // program counter

	public SmlCpu( )
	{
		acc = 0;
		pc = 0;
	}
}
	/*	some pseudocode
	void execute( instructionVal ){
		signal = cpu.result( instructionVal );
		moveData( signal.path, signal.cargo );
	}
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
		In : inp -> cpu
		Pr : cpu -> out
		Hl : cpu -> sml
		br : cpu -> cpu
		st : cpu -> ram
		Ld : ram -> cpu
		ma : cpu -> cpu

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

		 [cpu] result(instrVal){
		 	// assuming already indirected
		 	switch( storedInstrAlready ){
		 	 case Instr.INPUT:
		 	 	return new Signal( pair.I_C, instrVal );
		 	 case Instr.STORE:
		 	 	return new Signal( pair.C_R, instrVal );
			
	}
	*/
