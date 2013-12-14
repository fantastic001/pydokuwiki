
from dokuwiki.html import HTMLParser

from sys import argv as arguments

def main(): 
	print """
	Welcome to DokuWiki2HTML! 

	"""
	if arguments[1] == "--help": 
		print "Usage " + arguments[0] + " [wikifile] [output html file]" 
		exit(0) 
	f = open(arguments[1])
	p = HTMLParser()
	for line in f: 
		p.parse(line) 
	p.finish() 
	output = open(arguments[2])
	output.write(p.getOutput())
	output.close()
	f.close()

