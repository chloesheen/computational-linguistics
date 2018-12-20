"""
Assignment 4: Hashtag Tokenizer
Chloe Sheen
"""
import nltk
from nltk.corpus import brown
import urllib.request
from nltk.tag import hmm
import numpy as np

# 8 most frequent tags in news corpus, using Universal Tagset
tagged_words = brown.tagged_words(categories="news", tagset="universal")
ttable = nltk.FreqDist()
for(word, tag) in tagged_words:
	ttable[tag] += 1
for (tag, count) in ttable.most_common()[:8]:
	print(count, tag)

# 15 most frequent n, v, adj, adv in news corpus, using Universal Tagset
for pos in ['NOUN', 'VERB', 'ADJ', 'ADV']:
	ftable = nltk.FreqDist()
	for (word, tag) in tagged_words:
		if tag == pos:
			ftable[word+"/"+tag] += 1
	for (word_tag, count) in ftable.most_common()[:15]:
		print(count, word_tag)


def my_tagger(test):
	bts = brown.tagged_sents(tagset="universal")

	uTagr = nltk.UnigramTagger(bts)
	#print(uTagr.tag(test))
	#print(uTagr.evaluate([nltk.pos_tag(test, tagset="universal")]))

	bTagr = nltk.BigramTagger(bts)
	#print(bTagr.tag(test))
	#print(bTagr.evaluate([nltk.pos_tag(test, tagset="universal")]))

	patterns = [
	(r'[\.,:;?!]', '.'), # punctuation
	(r'^-?[0-9]+(.[0-9]+)?$', 'NUM'), # cardinal numbers
	(r'(The|the|A|a|An|an)$', 'DET'), # articles
	(r'(At|at|On|on|Out|out|Over|over|Per|per|That|that|Up|up|Down|down)$', 'PRT'), # articles
	(r'(Of|of|As|as|With|with|In|in|From|from|Until|until|At|at|On|on)$', 'ADP'), # adposition
	(r'(For|for|And|and|Nor|nor|But|but|Or|or|Yet|yet|So|so)$', 'CONJ'), # conjunction
	(r'.*able$', 'ADJ'), # adjectives
	(r'.*ness$', 'NOUN'), # nouns from adjectives
	(r'.*ly$', 'ADV'), # adverbs
	(r'(Be|be|Is|is|Are|are|Was|was|Were|were|Being|being|Does|does)$', 'VERB'), # be verbs
	(r'(Has|has|Have|have)$', 'VERB'), # have verbs
	(r'(Who|who|What|what)$', 'PRON'), # pronouns
	(r'(bites|bite)$','VERB'), # exception to the next rule for second text
	(r'.*s$', 'NOUN'), # plural noun
	(r'.*ing$', 'VERB'), # gerund
	(r'.*ed$', 'VERB'), # simple past
	(r'.*es$', 'VERB'), # 3rd person singular present
	(r'.*ould$', 'VERB'), # modal
	(r'.*\'s', 'NOUN'), # possessive noun
	(r'.*', 'NOUN') # noun default
	]

	reTagr = nltk.RegexpTagger(patterns)
	print(reTagr.tag(test))
	print(reTagr.evaluate([nltk.pos_tag(test, tagset="universal")]))
	print(reTagr.evaluate([nltk.pos_tag(test, tagset="")]))

	# we can now create a unigram tagger that backs off to a RE tagger
	myTagr = nltk.UnigramTagger(bts, backoff=reTagr)
	#print(myTagr.tag(test))
	#print(myTagr.evaluate([nltk.pos_tag(test, tagset="universal")]))

	# using NLTK's built-in tagger as gold standard
	gold_std = nltk.pos_tag(test, tagset="universal")
	#print(gold_std)

if __name__ == "__main__":
	url1 = urllib.request.urlopen('https://cs.brynmawr.edu/Courses/cs325/fall2018/Test.txt').read().decode().split()
	my_tagger(url1)
	url2 = urllib.request.urlopen('https://cs.brynmawr.edu/Courses/cs325/fall2018/test2.txt').read().decode().split()
	my_tagger(url2)
	"""text1 = "Ever since Trump was elected, it has been evident that his style alienates many college-educated suburban voters, \
	particularly women. This pattern is very much present in the latest data. Consider New Jersey’s Seventh District, which sprawls \
	west from Essex County, near New York, and is home to Trump’s Bedminster golf club. Tom Malinowski, a former Obama Administration \
	official, has established a narrow lead in the polls over Leonard Lance, a Republican congressman who has held the seat since 2009. \
	About four out of five voters in the district are white, and a majority have a college degree. Among white college-educated voters, \
	according to a poll by Monmouth University, Malinowski leads Lance by fifty-seven per cent to thirty-seven per cent. \
	There is also a big gender gap. Among women of all education levels, Malinowksi leads by seven points, whereas Lance is ahead among men by two points."

	#my_tagger(text1.split())

	text2 = "Oh, the Places You’ll Go! You have brains in your head. You have feet in your shoes. You can steer yourself Any direction you choose. \
	You’re on your own. And you know what you know. And YOU are the guy who’ll decide where to go. You’ll get mixed up, of course, as you already know. \
	You’ll get mixed up with many strange birds as you go. So be sure when you step. Step with care and great tact and remember that Life’s A Great Balancing Act.\
	And will you succeed? Yes! You will, indeed! (98 and ¾ percent guaranteed.) KID, YOU’LL MOVE MOUNTAINS!"
	#my_tagger(text2.split())
	"""
