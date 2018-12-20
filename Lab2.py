"""
CMSC 325 Assignment 2: Word and Sentence Segmentation
Chloe Sheen
"""
import nltk
from nltk.corpus import gutenberg
from nltk.corpus import inaugural
import re

def tokenize(rawtext):
	""" tokenizer(rawtext)
		input: rawtext
		output: prints number of sentences, words, vocabulary, average word length,
				and the length of the shortest and longest sentences after input
				has been tokenized
	"""
	mod_lines = re.sub('(\n)+', ' ', rawtext) 					# remove all newlines from text
	mod_boundaries = re.sub('[\!:\?]', '\n', mod_lines)			# replace sentence boundaries with \n
	mod_periods = re.sub('(?<!Mr)(?<!Mrs)(?<!Ms)(?<!Dr)[.]','\n',mod_boundaries) # replace . (exceptions)
	mod_dash = re.sub('-', ' ', mod_periods)					# replace dashes with a space
	mod_quotes = re.sub('[,;\'\"]', '', mod_dash)				# remove all , ; ' "

	sents = mod_quotes.split('\n')								# split into sentences
	for sent in sents:											# remove extraneous empty strings
		if sent is "":
			sents.remove(sent)
	print("# sentences:\t", len(sents))

	words = mod_quotes.replace('\n','').split(' ')				# split into tokens
	print("# words:\t", len(words))

	vocab = set([token.lower() for token in words])				# extract into vocabulary
	print("# vocabulary:\t", len(vocab))
	avg_word_len = len(words)/len(sents)
	print("Average word length of sentence:\t", avg_word_len)

	# finding the shortest and longest sentences
	wordlist_list = [sent.split(" ") for sent in sents]			# a list of words in each sentence
	for wordlist in wordlist_list:								# remove extraneous empty strings
		for word in wordlist:
			if word == "":
				wordlist.remove(word)

	num_words = [len(wordlist_list[i]) for i in range(len(sents))]	# a list of the length of the words
	shortest = min(num_words)										# in each sentence, to apply min/max
	longest = max(num_words)
	print("Length of shortest sentence: ", shortest)
	print("Length of longest sentence: ", longest)

def nltk_tokenize(text):
	""" nltk_tokenizer(text)
		input: text
		output: prints (1) pre-segmented data in NLTK of the texts and
					   (2) data retrieved from NLTK's tokenizer
	"""
	print("PRE-SEGMENTED NLTK")
	print("# sentences:\t", len(gutenberg.sents(text)))
	print("# words:\t", len(gutenberg.words(text)))

	print("NLTK TOKENIZER")
	print("# sentences:\t", len(nltk.sent_tokenize(gutenberg.raw(text))))
	print("# words :\t", len(nltk.word_tokenize(gutenberg.raw(text))))

if __name__ == '__main__':
	# starting with a small text
	# print(tokenize("I am Chloe Sheen. Chloe Sheen is me. You are not Chloe."))

	print("********************")
	print("TOKENIZE - [Emma]")
	tokenize(gutenberg.raw("austen-emma.txt"))
	nltk_tokenize("austen-emma.txt")

	""" need to change "gutenburg" to "inaugural" to run
	print("********************")
	print("TOKENIZE - [Inaugural Speech]")
	tokenize(inaugural.raw("2009-Obama.txt"))
	nltk_tokenize("2009-Obama.txt")
	"""
	print("********************")
	print("TOKENIZE - [Alice's Adventures]")
	tokenize(gutenberg.raw("carroll-alice.txt"))
	nltk_tokenize("carroll-alice.txt")

	print("********************")
	print("TOKENIZE - [Hamlet]")
	tokenize(gutenberg.raw('shakespeare-hamlet.txt'))
	nltk_tokenize('shakespeare-hamlet.txt')
