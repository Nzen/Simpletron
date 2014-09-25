package sml;

public enum Isa
{
	READ (1000),
	WRITE (1100),
	LOAD (2000),
	STORE (2100),
	ADD (3000),
	SUBTRACT (3100),
	DIVIDE (3200),
	MULTIPY (3300),
	MODULUS (3400),
	BRANCH (4000),
	BRANCHNEG (4100),
	BRANCHZERO (4200),
	HALT (4300);

	private final int val;
	Isa( int value )
	{
		this.val = value;
	}

	public int val()
	{
		return val;
	}

	public int divisor()
	{
		return 100; // 2311/100 = 23
	}
}
/*
	Works to my current satisfaction. The int var for addresses
	will happen either way, since these come from files or input
	I'm pretty pleased that I don't have to do modulus math now :B

	public static void testIsa()
	{
		Isa opV = Isa.ADD;
		int op = opV.val() + 5;
		System.out.println( op );
		System.out.println( op - opV.val() );
		System.out.println( op/opV.divisor() );
		// OUT
		3005
		5
		30
	}
*/