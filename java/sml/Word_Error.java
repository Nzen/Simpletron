package sml;

// simple wrapper for a value and an error flag

public class Word_Error
{
	private int val;
	private SmlError status;
	
	public Word_Error( int v, SmlError s )
	{
		val = v;
		status = s;
	}

	public int word()
	{
		return val;
	}

	public SmlError flag()
	{
		return status;
	}
}
