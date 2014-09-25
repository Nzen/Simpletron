package sml;

//package java;

public class SmlMem
{
	private int[] ram;
	private int SIZE;
	public int MAX = 9999;

	public SmlMem( int size )
	{
		if (badSize(size) )
			System.exit(0);
		SIZE = size;
		ram = new int[ SIZE ];
	}

	public int readMem( int address )
	{
		if ( badAddr( address ) )
		{
			return MAX + 1;//SmlError.BAD_ADDR; or val error struct?
		}
		else
		{
			return ram[ address ];
		}
	}

	public SmlError setMem( int address, int newVal )
	{
		if ( underflow( newVal ) )
			return SmlError.UNDERFLOW;
		else if ( overflow( newVal ) )
			return SmlError.OVERFLOW;
		else if ( badAddr( address ) )
		{
			return SmlError.BAD_ADDR;
		}
		else
		{
			ram[ address ] = newVal;
			return SmlError.NONE;
		}
	}

	private boolean underflow( int val )
	{
		return val < MAX * -1;
	}

	private boolean overflow( int val )
	{
		return val > MAX;
	}

	public boolean badAddr( int tried )
	{
		return badSize( tried ) || tried >= ram.length;
	}

	private boolean badSize( int size )
	{
		return size <= 0;
	}

	// --	--	--

	private int t_badSize()
	{
		int bad = 0;
		if ( ! badSize( -100 ) )
			bad++;
		if ( badSize( 223 ) )
			bad++;
		return bad;
	}

	private int t_badAddr( )
	{
		int bad = 0;
		if ( ! badAddr( -100 ) )
			bad++;
		if ( badAddr( SIZE + 223 ) )
			bad++;
		return bad;
	}

	private int t_flowProbs()
	{
		int bad = 0;
		if ( ! underflow( -MAX - 100 ) )
			bad++;
		if ( underflow( -100 ) )
			bad++;
		if ( ! overflow( MAX + 223 ) )
			bad++;
		if ( overflow( 223 ) )
			bad++;
		return bad;
	}

	private int t_readMem()
	{
		int bad = 0;
		if ( ! overflow(readMem( SIZE + 50 )) )
			bad++;
		int val = 39;
		int ind = 3;
		int temp = ram[ ind ];
		ram[ ind ] = val;
		if ( readMem( ind ) != val )
			bad++;
		ram[ ind ] = temp;
		ind = 0;
		temp = ram[ ind ];
		ram[ ind ] = val;
		if ( readMem( ind ) != val )
			bad++;
		ram[ ind ] = temp;
		return bad;
	}

	private int t_setMem()
	{
		int bad = 0;
		int addr = -1;
		int val = 38;
		int temp;
		if ( setMem( addr, val ) != SmlError.BAD_ADDR )
			bad++;
		addr = 0;
		val = -10000000;
		if ( setMem( addr, val ) != SmlError.UNDERFLOW )
			bad++;
		addr = 10;
		val = -val;
		if ( setMem( addr, val ) != SmlError.OVERFLOW )
			bad++;
		temp = ram[ addr ];
		val = 40;
		if ( setMem( addr, val ) != SmlError.NONE )
			bad++;
		else if ( ram[ addr ] != val )
			bad++;
		ram[ addr ] = temp;
		return bad;
	}
	/*
	private int t_readMem()
	{
		int bad = 0;
		if (  )
			bad++;
		return bad;
	}
	*/
	public int testMem()
	{
		int bad = 0;
		bad += t_badSize();
		bad += t_badAddr();
		bad += t_flowProbs();
		bad += t_readMem();
		bad += t_setMem();
		return 0;
	}
}




































