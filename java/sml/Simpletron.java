package Sml;


//package java;

public class Simpletron
{
	private static String intro = "*** Welcome to Simpletron! ***\n*** Please enter your program one instruction ***\n*** (or data word) at a time into the input ***\n*** text field. I will display the location ***\n*** number and a question mark (?). You then ***\n*** type the word for that location. Press the ***\n*** Done button to stop entering your program. ***";
	private static String endLoad = "*** Program loading completed ***";
	private static String beginExe = "*** Program execution begins ***";

	public static void main( String[] args )
	{
		deitelVersion();
	}

	public static void deitelVersion( )
	{
		SmlCpu brain = new SmlCpu();
		SmlMem memory = new SmlMem( 30 );
		Loader stdin = new Loader();
		System.out.println( "\n" + intro );
		System.out.println( "\n It actually means put the value -99999 to FINISH" ); // FIX
		System.out.println( "\t" + stdin.getLine() );
		System.out.println( "\n" + endLoad );
		System.out.println( "\n" + beginExe );
	}
}