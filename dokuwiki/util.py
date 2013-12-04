
def countChars(s, cc): 
	"""
	Counts how many characters cc are there in s 

	s: string 
	cc: character to count 

	returns: integer 
	"""
	count = 0 
	for c in s: 
		if c == cc:
			count = count + 1 
	return count 
