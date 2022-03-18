# ircmsg_o_notation
An example that O(n) does not work all the time on a real code.

There are 2 realisations of raw irc messages parser:

1: O(n) algorithm. Each character would be passed only once.
	
2: Uses build-in fast methods of str-type. Wrote in clear-code style. Complexity of the code is:

	2.1: Passing through each character to split tags, command, params and trailing parts. O(n)
	2.2: Passing second time through whole tags to separate each. +O(t)
	2.3: Passing third time through whole tags to separate keys and values. +O(t1)
	2.4: Passing three times through each value unescaping it. +O(t2)
	2.6: Passing through params. +O(p)
	2.5: Passing through prefix. +O(x)
		
	In the worst case the complexity is O(n+t+t1+t2+p+x). 
	Also it's the worst when each part is whole message, so complexity is O(6n).

 But if we will try to capture the time each algorithm takes to be passed, we'll see that:

	4-characters-length:        18% 2nd faster over 1st
	600-characters-length:     800% 2nd faster over 1st
	205000-characters-length: 2300% 2nd faster over 1st
	
But we expected that relative performance between the algorithms would not be changing during length's increasing.

		expected:                    see:
	  ________________________     ________________________
	  |                      |     |                     /|
	  |                      |     |                  /   |
	  |                      |     |               /      |
	  |                      |     |            /         |
	  |                      |     |         /            |
	  |______________________|     |      /               |
	  |                      |     |   /                  |
	y^|                      |   y^|/                     |
	x>------------------------   x>------------------------
	
	Where x - message's length. y - time-of-2st devided by time-of-1st.
	

And that absolute time of the 2nd will increase about 6 times faster than of the 1st. 

Run test/preformance.py 
