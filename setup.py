from setuptools import setup, find_packages
setup(
	name = "PyDokuwiki",
	version = "0.1",
	packages = find_packages(),
	author = "Stefan Nozinic",
	author_email = "stefan@lugons.org",
	description = "Python module and scripts for manipulating dokuwiki formated text (seen in dokuwiki's wiki pages etc).",
	keywords = "wiki dokuwiki text parsing",
	#entry_points = {
	#	'console_scripts': [
	#		"dokuwiki2html = dokuwiki.dokuwiki2html:main", 
	#	]
	#}
	scripts = ["./dokuwiki2html"]
)


