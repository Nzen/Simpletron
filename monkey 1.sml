1100
1029
3002
4027
2127
3126
4024
4124
4022
2021
4120
4020
4121
0
0
0
0
0
0
0
0
5
6
0
5
0
1
1
3
0
##
0 print from 0 # should be 29 or 30 // Did I make these by hand?
1 input to 29
2 goto 2	# infinite loop here, should be 3
3 load acc from 27	# where did 28 go?
4 subtract acc & from 27 #
5 if acc negative goto 26 # should be go to 6 & where's 25?
6 load acc from 24
7 store acc into 24 # should point at 29
8 load acc from 22
9 add acc & num from 21
10 store acc into 20
11 load acc from 20
12 store acc into 21
13 ..0

3 print 5	# ORIGINAL simple code
6 input x
7 goto 9
9 if 3 == 1 goto 10
10 let x = 5
11 let y = 6 + 5
53 end

20 ..0 Y
21 ..5 # should have pointed at 24
22 ..6 6
23 ..0
24 ..5 5
25 ..0
26 ..1 __
27 ..1 1
28 ..3 3
29 ..0 X
