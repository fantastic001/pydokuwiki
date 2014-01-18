
from dokuwiki.html import HTMLParser

import argparse


# Some constans 

default_style = """

body 
{
	background-color: white;
}

h1 h2 h3 h4 h5 h6 
{
	color: #800000;
}

"""

def main(): 
	print """
	Welcome to DokuWiki2HTML! 

	"""
	parser = argparse.ArgumentParser(description='Convert dokuwiki pages to HTML')
	parser.add_argument('--input', help='Input dokuwiki file', required=True)
	parser.add_argument('--output', help="Specify output file (if file does not exist, it'll be created)", required=True)
	parser.add_argument("--style", help="Specify stylesheet file to be used (if not specified, it will not be used, if specified default, default will be used)")
	args = parser.parse_args()

	f = open(args.input, "r")
	p = HTMLParser()
	for line in f: 
		p.parse(line) 
	p.finish() 
	output = open(args.output, "w")

	# Read stylesheet
	style = None 
	if args.style != None: 
		if args.style == "default": 
			style = default_style
		else: 
			with open(args.style) as mystyle:
				style = mystyle.read()

	output.write(p.getOutput(stylesheet=style))
	output.close()
	f.close()

