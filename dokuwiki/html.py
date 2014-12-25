
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

class HTMLLineParser(LineParser): 
	
	def onStart(self): 
		self.output = ""
	def onNormal(self, text): 
		self.output += text
	def onItalicStart(self):
		self.output += "<i>"
	def onItalicEnd(self): 
		self.output += "</i>"
	def onBoldStart(self): 
		self.output += "<strong>"
	def onBoldEnd(self):
		self.output += "</strong>"
	def onUnderlineStart(self): 
		self.output += "<u>"
	def onUnderlineEnd(self): 
		self.output += "</u>"
	def onLink(self, url, title): 
		self.output += "<a href='" + url + "'>" + title + "</a>"
	def onImage(self, params):	
		self.output += params
	def getOutput(self): 
		return self.output

class HTMLParser(Parser): 
	def onDocumentStart(self): 
		self.output = ""
	def onHeading(self, level, text):
		self.output += "<h" + str(7 - level) + ">" + text + "</h" + str(7 - level) + ">\n"
	def onListStart(self, mode): 
		self.output += "<ul>\n"
	def onListEnd(self): 
		self.output += "</ul\n>"
	def onListItem(self, level, text): 
		self.output += "<li>" + text + "</li>\n"
	def onCodeStart(self, language, filename): 
		self.output += "<pre>\n"
	def onCode(self, text): 
		self.output += text + "\n"
	def onCodeEnd(self): 
		self.output += "</pre>\n"
	def onParagraphStart(self): 
		self.output += "<p>"
	def onParagraphEnd(self): 
		self.output += "</p>\n"
	def onText(self, text):
		t = html_encode(text) # encode text for HTML 
		l = HTMLLineParser(t)
		self.output += l.getOutput()
	def onDocumentEnd(self): 
		pass
	
	def getOutput(self, stylesheet=None): 
		head = "<html>\n<head>\n<title>WIKI Page</title>\n"
		head+= '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n'
		if stylesheet != None: 
			head += "<style type='text/css'>\n" + stylesheet + "\n</style>\n"
		head += "</head>\n"
		return head + "<body>\n" + self.output + "</body></html>"
