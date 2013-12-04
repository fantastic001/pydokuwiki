
import re 

class LineElement(object): 
	
	class Mode(object): 
		ITALIC, BOLD, UNDERLINE, LINK, NORMAL = range(5)

	def __init__(self, e): 
		self.element = e 
		
		italic = re.compile(r"^//$")
		underline = re.compile(r"^__$")
		bold = re.compile(r"^\*\*$")
		link = re.compile("^\[\[([^|]+)\|?(.*)\]\]$")

		if italic.match(e): 
			self.mode = LineElement.Mode.ITALIC 
		elif underline.match(e): 
			self.mode = LineElement.Mode.UNDERLINE
		elif bold.match(e): 
			self.mode = LineElement.Mode.BOLD
		elif link.match(e): 
			match = link.match(e) 
			self.url = match.group(1) 
			self.desc = match.group(2)
			self.mode = LineElement.Mode.LINK
		else: 
			self.mode = LineElement.Mode.NORMAL

	def getMode(self): 
		"""
		Returns mode which is attribute of class LineElement.Mode 

		return: LineElement.Mode
		"""
		return self.mode

	def getURL(self): 
		"""
		Returns URL if getMode() is LineElement.Mode.LINK, otherwise returns None 

		return: URL - string 
		"""
		if self.mode == LineElement.Mode.LINK: 
			return self.url.strip()
		else: 	
			return None

	def getTitle(self): 
		"""
		Returns page title if getMode() is LineElement.Mode.LINK, otherwise returns None 

		return: title - string 
		"""
		if self.mode == LineElement.Mode.LINK: 
			return self.desc.strip()
		else: 
			return None
