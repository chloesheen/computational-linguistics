"""
Assignment 5
Chloe Sheen
"""
import nltk
import urllib.request
import string

def parse(input):
	grammar = nltk.CFG.fromstring(
	"""
	S -> NP VP | Aux NP VP | Aux NP NP | WH_NP VP | WH_NP Aux WH_NP
	NP -> PreDet NP | Det N | N | ProperNoun
	VP -> V | V NP | V WH_NP
	WH_NP -> WH NP | WH
	WH -> "what" | "who"
	PreDet -> "all"
	V -> "is" | "are" | "has" | "swims" | "swim" | "flies" | "fly" | "have" | "eat" | "bite" | "walk" | "walks" | "bites"
	Det -> "a" | "an" | "the"
	ProperNoun -> "socrates" | "deepak" | "rover" | "snoopy" | "tweety" | "polly"
	N -> "fish" | "animal" | "animals" | "bird" | "birds" | "gills" | "mammals" | "humans" | "human" | "dogs" | "collie" | "collies" | "beagle" | "beagles" | "canaries" | "canary" | "parrots" | "parrot" | "canines" | "hair" | "feathers" | "biped"
	Aux -> "does" | "is"

	""")

	parser_top_down = nltk.RecursiveDescentParser(grammar)
	instantiate_parser = grammar.productions()
	sents = [sent.split() for sent in input]

	for sent in sents:
		sent = [s.translate(str.maketrans('','',string.punctuation)).lower() for s in sent]
		for p in parser_top_down.parse_one(sent):
			print(p)
		print("\n")

if __name__ == "__main__":
	test_file = open('test.txt')
	test_url = urllib.request.urlopen('https://cs.brynmawr.edu/Courses/cs325/fall2018/test2.txt').read().decode()
	parse(test_file)
