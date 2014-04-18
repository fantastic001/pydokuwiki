
import re 

from .elements import LineElement

from .util import countChars



class LineSegmenter(object): 
	
	def __init__(self, line=""): 
		"""
		Initializes parser 

		line: string representing one line 
		"""
		self.line = line 
		self.elements = []
	
	def prepare(self, line=""): 
		"""
		Prepares line for parsing (makes sure that every link if in [[...]] form) 

		line: string representing line for preparing (default: '', using line defined in constructor) 

		return: new line
		"""
		if line == "": 
			line = self.line 
		line = re.sub(r"([^\[]{2} *|^)((http|https|ftp)://[^ ]+)", r"\1[[\2]]", line)
		return line


	def parse(self, line=""): 
		"""
		Parses line and returns list of elements
		
		line: string representing line (default: "", using line defined in constructor)

		returns: list of elements

		e.g. ["//", "foo", "//", " bar ", "__", "underlined", "__"]
		"""
		# For parsing there are several states
		# States: 
		# 	0: 	normal character 
		# 	1: 	first token found 
		# 	2: 	Second token found 
		# 	-1: 	Link state 
		# 	-2: 	End link token found 
		elements = []
		if line == "" or line == None: 
			line = self.line
		# Replace all URLs with appropriate syntax 
		# line = re.sub(r"[^\[]{2}((http|https|ftp|ssh|mail)://)?(\w+(\.\w+)+(/[^ ]*)?)", r"[[\1\3]]", line)
		current = ""
		token = ""
		state = 0
		for c in line: 
			if c in "/*_[" and state == 0: 
				state = 1
				token = c 
			elif c == token and state == 1: 
				state = 0 
				if current != "": elements.append(current)
				if token == "[": 
					current = "[["
					state = -1
					continue
				elements.append(token + token) 
				current = ""
				token = ""
			elif c in "/_*" and c != token and state == 1: 
				current += token 
				token = c
			elif c == "]" and state == -1: 
				state = -2 
				current = current + c 
			elif c == "]" and state == -2: 
				current = current + c 
				elements.append(current)
				state = 0
				current = ""
			else:
				if token in "/_*": 
					current += token 
				current = current + c
				token = ""
				if state > 0: state = 0
		if current != "": 
			elements.append(current)
		self.elements = elements 
		return elements

def WikiSyntaxError(Exception):
	"""
	Exception which is raised if syntax error was detected
	"""


class LineParser(object): 
	def __init__(self, line): 
		self.onStart()
		
		bold = False
		italic = False
		underline = False

		l = LineSegmenter()
		t = l.prepare(t) 
		for e in l.parse(t): 
			element = LineElement(e) 
			if element.getMode() == LineElement.Mode.NORMAL: 
				self.onNormal(e)
			elif element.getMode() == LineElement.Mode.ITALIC and not italic: 
				italic = True
				self.onItalicStart()
			elif element.getMode() == LineElement.Mode.ITALIC and italic: 
				self.output += "</i>"
				self.onItalicEnd()
			elif element.getMode() == LineElement.Mode.BOLD and not bold: 
				bold = True
				self.onBoldStart()
			elif element.getMode() == LineElement.Mode.BOLD and bold:
				bold = False 
				self.onBoldEnd()
			elif element.getMode() == LineElement.Mode.UNDERLINE and not underline: 
				underline = True
				self.onUnderlineStart()
			elif element.getMode() == LineElement.Mode.UNDERLINE and underline: 
				underline = False
				self.onUnderlineEnd()
			elif element.getMode() == LineElement.Mode.LINK: 
				link_title = element.getTitle() 
				if link_title == "" or link_title == None: 
					link_title = element.getURL()
				self.onLink(element.getURL(), link_title)
			else: 
				raise WikiSyntaxError()
	def onStart(self): pass
	def onNormal(self, text): pass
	def onItalicStart(self): pass
	def onItalicEnd(self): pass
	def onBoldStart(self): pass
	def onBoldEnd(self): pass
	def onUnderlineStart(self): pass
	def onUnderlineEnd(self):pass 
	def onLink(self, url, title): pass

class Parser(object): 
	"""
	Parser class which is used for parsing wiki files. It uses LineParser for parsing individual lines and keeps track of 
	list startings, headings etc... 

	This class just calls its methods for some cases (like on headings, list startings etc...) and other classes have to inherit it.
	This class is also untestable and DummyParser was created for that. 

	Every class which inherits this class has to implement its own representation of following methods: 
	
		onDocumentStart()
		onHeading(level, text) 
		onListStart(mode) - mode: one from modes.ListMode
		onListEnd()
		onListItem(level, text) - level starts at 0
		onCodeStart(language, filename)
		onCode(line)
		onCodeEnd()
		onParagraphStart()
		onParagraphEnd()
		onText(text) called in all other cases
		onDocumentEnd()
	
	"""

	
	def __init__(self): 
		"""
		Initializes parser
		"""

		# Mode: 
		# 	0: none
		# 	1: list
		#	2: code
		# 	3: paragraph
		# 	4: code activated with <code> tag

		self.mode = 0
		self.list_mode = None
		self.code_filename = "" # for later usage 
		self.code_language = "" # for later usage 

		# RE patterns 
		self.heading = re.compile(r"^ *(======|=====|====|===|==|=)(.+[^=])(======|=====|====|===|==|=) *$")
		self.list_item = re.compile(r"^(	+|  +)(\*|-) (.*)$")
		self.code = re.compile(r"^(<code>|</code>) *$")
		self.code_item = re.compile(r"^(	|  +)(.*)$")
		self.paragraph_break = re.compile(r"^ *$")
		
		self.onDocumentStart()
	def parse(self, line=""): 
		"""
		Parses given line and calls apropirate function
		"""
		hm = self.heading.match(line) 
		lm = self.list_item.match(line) 
		cm = self.code.match(line) 
		cim = self.code_item.match(line)
		pm = self.paragraph_break.match(line)
		
		mode = self.mode
		
		#print line, 

		if hm and mode == 0: 
			#print "h->0"
			self.onHeading(countChars(hm.group(1), "="), hm.group(2))
			self.mode = 0
		elif hm and mode == 3: 
			#print "3->h"
			self.onParagraphEnd
			self.onHeading(countChars(hm.group(1), "="), hm.group(2))
			self.mode = 0
		elif hm and mode == 1:
			#print "1->h"
			self.onListEnd()
			self.onHeading(countChars(hm.group(1), "="), hm.group(2))
			self.mode = 0
		elif lm and mode == 0: 
			#print "0->1"
			self.mode = 1 
			self.onListStart(0)
			self.onListItem(0, lm.group(3))
		elif lm and mode == 3: 
			#print "3->1"
			self.mode = 1
			self.onParagraphEnd()
			self.onListStart(0)
			self.onListItem(0, lm.group(3))
		elif lm and mode == 1: 
			self.onListItem(0, lm.group(3))
		elif cm and mode != 4 and cm.group(1) != "</code>": 
			self.mode = 4
			if mode == 3: 
				#print "3->4"
				self.onParagraphEnd()
			elif mode == 1: 
				#print "1->2"
				self.onListEnd()
			self.onCodeStart("", "") 
		elif cm and mode == 4 and cm.group(1) == "</code>": 
			#print "4->0"
			self.mode = 0 
			self.onCodeEnd()
		elif cim and mode == 0:
			#print "0->2"
			#print "item matched"
			self.mode = 2
			self.onCodeStart("", "")
			self.onCode(cim.group(2))
		elif cim and mode == 1: 
			#print "1->2"
			#print "item matched"
			self.mode = 2 
			self.onListEnd()
			self.onCodeStart("", "") 
			self.onCode(cim.group(2))
		elif cim and mode == 3: 
			#print "3->2"
			#print "item matched"
			self.mode = 2 
			self.onParagraphEnd()
			self.onCodeStart("", "")
			self.onCode(cim.group(2))
		elif cim and mode == 2: 
			#print "item matched"
			self.onCode(cim.group(2))
		elif pm and mode == 1: 
			#print "1->0"
			self.mode = 0 
			self.onListEnd()
		elif pm and mode == 2: 
			#print "2->0"
			self.mode = 0 
			self.onCodeEnd()
		elif pm and mode == 3: 
			#print "3-0"
			self.mode = 0
			self.onParagraphEnd()
		elif mode == 0: 
			#print "0->3"
			self.mode = 3
			self.onParagraphStart()
			self.onText(line)
		elif mode == 1: 
			#print "1->3"
			self.mode = 3 
			self.onListEnd()
			self.onParagraphStart()
			self.onText(line)
		elif mode == 2 and not cim: 
			#print "2->3"
			self.mode = 3 
			self.onCodeEnd()
			self.onParagraphStart()
			self.onText(line)
		elif mode == 4: 
			#print "item matched"
			self.onCode(line)
		else: 
	                self.onText(line)
	def finish(self): 
		if self.mode == 3: 
			self.mode = 0 
			self.onParagraphEnd()
		elif self.mode == 1: 
			self.mode = 0 
			self.onListEnd()
		elif self.mode == 2: 
			self.mode = 0 
			self.onCodeEnd()
		self.onDocumentEnd()

	def onDocumentStart(self): pass 
	def onHeading(self, level, text): pass
	def onListStart(self, mode): pass
	def onListEnd(self): pass
	def onListItem(self, level, text): pass
	def onCodeStart(self, language, filename): pass
	def onCode(self, text): pass
	def onCodeEnd(self): pass
	def onParagraphStart(self): pass
	def onParagraphEnd(self): pass
	def onText(self, text): pass
	def onDocumentEnd(self): pass
