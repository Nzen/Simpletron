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
0 print from 0
1 input to 29
2 goto 2	# where did 28 go?
3 load acc from 27
4 subtract acc & from 27
5 if acc negative goto 26 # & where's 25?
6 load acc from 24
7 store acc into 24 # not storing somewhere else, in fact it should point at "0", given above
8 load acc from 22
9 add acc & from 21
10 store acc into 20
11 load acc from 20
12 store acc into 21
13 ..0

3 print 5
6 input x
7 goto 9
9 if 3 == 1 goto 10
10 let x = 5
11 let y = 6 + 5
53 end

21 ..5
22 ..6
23 ..0
24 ..5
25 ..0
26 ..1
27 ..1
28 ..3
29 ..0
