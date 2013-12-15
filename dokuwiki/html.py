
from .parsers import * 
from .elements import * 
def html_encode(text): 
	"""
	Encodes HTML entities by replacing each of them with appropriate entity 

	text: string to encode 
	return: new encoded string 
	"""
	new = text
	entities = {
		">": "&gt;", 
		"<": "&lt;", 
		"&": "&amp;"
	}
	for e in entities.keys(): 
		new = new.replace(e, entities[e]) 
	return new

class HTMLParser(Parser): 
	def onDocumentStart(self): 
		self.output = "<html>\n<head>\n<title>WIKI Page</title>\n"
		self.output += '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
		self.output += "</head>\n<body>\n"
	def onHeading(self, level, text):
		self.output += "<h" + str(7 - level) + ">" + text + "</h" + str(7 - level) + ">\n"
	def onListStart(self, mode): 
		self.output += "<ul>\n"
	def onListEnd(self): 
		self.output += "</ul\n>"
	def onListItem(self, level, text): 
		self.output += "<li>" + text + "</li>\n"
	def onCodeStart(self, language, filename): 
		self.output += "<code>\n"
	def onCode(self, text): 
		self.output += text
	def onCodeEnd(self): 
		self.output += "</code>\n"
	def onParagraphStart(self): 
		self.output += "<p>"
	def onParagraphEnd(self): 
		self.output += "</p>\n"
	def onText(self, text):
		bold = False
		italic = False
		underline = False

		t = html_encode(text) # encode text for HTML 
		l = LineParser()
		t = l.prepare(t) 
		for e in l.parse(t): 
			element = LineElement(e) 
			if element.getMode() == LineElement.Mode.NORMAL: 
				self.output += e 
			elif element.getMode() == LineElement.Mode.ITALIC and not italic: 
				self.output += "<i>"
			elif element.getMode() == LineElement.Mode.ITALIC and italic: 
				self.output += "</i>"
			elif element.getMode() == LineElement.Mode.BOLD and not bold: 
				self.output += "<strong>"
			elif element.getMode() == LineElement.Mode.BOLD and bold:
				self.output += "</strong>"
			elif element.getMode() == LineElement.Mode.UNDERLINE and not underline: 
				self.output += "<u>"
			elif element.getMode() == LineElement.Mode.UNDERLINE and underline: 
				self.output += "</u>"
			elif element.getMode() == LineElement.Mode.LINK: 
				link_title = element.getTitle() 
				if link_title == "" or link_title == None: 
					link_title = element.getURL()
				self.output += "<a href='" + element.getURL() + "'>" + link_title + "</a>"
			else: 
				raise WikiSyntaxError()
	def onDocumentEnd(self): 
		self.output += "</body></html>"
	
	def getOutput(self): 
		return self.output
