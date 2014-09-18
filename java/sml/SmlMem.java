package Sml;

//package java;

public class SmlMem
{
	private int[] ram;
	private int SIZE;

	public SmlMem( int size )
	{
		if (badSize(size) )
			System.exit(0);
		SIZE = size;
		ram = new int[ SIZE ];
	}

	public boolean badSize( int size )
	{
		return size <= 0;
	}
}