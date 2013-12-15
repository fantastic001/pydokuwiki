from dokuwiki.parsers import * 
from dokuwiki.html import *
from dokuwiki.elements import * 

import unittest 

class TestLineParser(unittest.TestCase): 
	def setUp(self): 
		self.parser = LineParser()

	def test_normal(self): 
		self.assertEqual(self.parser.parse("foo bar"), ["foo bar"])
	
	def test_bold(self): 
		self.assertEqual(self.parser.parse("**foo** bar"), ["**", "foo", "**", " bar"])
	
	def test_italic(self): 
		self.assertEqual(self.parser.parse("//foo bar//"), ["//", "foo bar", "//"])

	def test_bold_italic(self): 
		self.assertEqual(self.parser.parse("**//foo bar//**"), ["**", "//", "foo bar", "//", "**"])

	def test_underline(self): 
		self.assertEqual(self.parser.parse("__foo bar__"), ["__", "foo bar", "__"])

	def test_bold_italic_underline(self): 
		self.assertEqual(self.parser.parse("**//__foo bar__//**"), ["**", "//", "__", "foo bar", "__", "//", "**"])
	
	def test_links(self): 
		self.assertEqual(self.parser.parse("[[http://www.google.com|This Link points to google]]"), ["[[http://www.google.com|This Link points to google]]"])
	
	def test_prepare(self): 
		self.assertEqual(self.parser.prepare("http://www.google.com"), "[[http://www.google.com]]")
		self.assertEqual(self.parser.prepare("http://www.google.com/hey"), "[[http://www.google.com/hey]]")
		self.assertEqual(self.parser.prepare("[[http://www.google.com]]"), "[[http://www.google.com]]")
		self.assertEqual(self.parser.prepare("http://www.google.com [[link]]"), "[[http://www.google.com]] [[link]]")
		self.assertEqual(self.parser.prepare("[[link]] http://www.google.com"), "[[link]] [[http://www.google.com]]")
		self.assertEqual(self.parser.prepare("[[ http://www.google.com ]]"), "[[ http://www.google.com ]]")


class DummyParser(Parser): 
	def onDocumentStart(self): 
		self.m = 0
	def onHeading(self, level, text): 
		self.level = level 
		self.text = text
	def onListStart(self, mode):
		self.m = 1
	def onListEnd(self):
		self.m = 0
	def onListItem(self, level, text):  
		self.text = text
	def onCodeStart(self, language, filename):
		self.m = 2
	def onCodeEnd(self): 
		self.m = 0
	def onParagraphStart(self): 
		self.m = 3
	def onParagraphEnd(self):
		self.m = 0
	def onText(self, text):
		self.text = text
	def onCode(self, text): 
		self.text = text

class TestParser(unittest.TestCase):
	def setUp(self): 
		self.p = DummyParser()
	def test_heading(self): 
		p = DummyParser() 
		p.parse("===HI===") 
		self.assertEqual((p.text, p.level), ("HI", 3))
	def test_transitions(self):
		self.p.parse("  * item1") 
		self.assertEqual((self.p.m, self.p.text), (1, "item1"))
		self.p.parse("  * item 2") 
		self.assertEqual((self.p.m, self.p.text), (1, "item 2"))
		self.p.parse("hi") 
		self.assertEqual((self.p.m, self.p.text), (3, "hi"))
		self.p.parse("<code>") 
		self.p.parse("bash") 
		self.assertEqual((self.p.m, self.p.text), (2, "bash"))
		self.p.parse("</code>") 
		self.assertEqual(self.p.m, 0)
		self.p.parse("another paragraph") 
		self.assertEqual((self.p.m, self.p.text), (3, "another paragraph"))
		self.p.parse("")
		self.assertEqual(self.p.m, 0)
		self.p.parse("  bash") 
		self.assertEqual((self.p.m, self.p.text), (2, "bash"))
		self.p.parse("new paragraph") 
		self.assertEqual((self.p.m, self.p.text), (3, "new paragraph")) 
		self.p.parse("  - num") 
		self.assertEqual((self.p.m, self.p.text), (1, "num"))

class TestHTML(unittest.TestCase): 
	def setUp(self): pass 
	def test_html_encode(self): 
		self.assertEqual(html_encode(">"), "&gt;")
		self.assertEqual(html_encode("<"), "&lt;")
		self.assertEqual(html_encode("&"), "&amp;")
		self.assertEqual(html_encode("> <"), "&gt; &lt;")
		self.assertEqual(html_encode("> &"), "&gt; &amp;")
		self.assertEqual(html_encode("< &"), "&lt; &amp;")
		self.assertEqual(html_encode("> < &"), "&gt; &lt; &amp;")


class TestLineElement(unittest.TestCase): 
	def test(self): 
		e = LineElement("//")
		self.assertEqual(e.getMode(), LineElement.Mode.ITALIC)

		e = LineElement("**")
		self.assertEqual(e.getMode(), LineElement.Mode.BOLD)

		e = LineElement("__")
		self.assertEqual(e.getMode(), LineElement.Mode.UNDERLINE)

		e = LineElement("[[www.google.com | google]]")
		self.assertEqual(e.getMode(), LineElement.Mode.LINK)
		self.assertEqual(e.getURL(), "www.google.com")
		self.assertEqual(e.getTitle(), "google")
		
		e = LineElement("[[www.google.com]]")
		self.assertEqual(e.getMode(), LineElement.Mode.LINK)
		self.assertEqual(e.getURL(), "www.google.com")
		self.assertEqual(e.getTitle(), "")
# Run unittest 
unittest.main()
	
