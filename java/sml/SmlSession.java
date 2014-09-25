package sml;

public class SmlSession
{
	public static void main( String[] args )
	{
		// I'd rather handle argument flags here than in simpletron
		//Simpletron atari = new Simpletron( SmlFlag.HAND );
		SmlMem bla = new SmlMem( 33 );
		System.out.println( bla.testMem() );
	}
}