import nltk
from nltk.corpus import brown

cat = brown.categories()

# raw text of news category
words = brown.words(categories='news')
sents = brown.sents(categories='news')

# tagged words and sentences, using original Brown Tagset
tagged_words = brown.tagged_words(categories="news")
tagged_sents = brown.tagged_sents(categories="news")

# tagged words and sentences, using simplified tags --> has been since modified to universal tagset
twords = brown.tagged_words(categories="news", tagset="universal")

# frequency table
ftable = nltk.FreqDist(words)
"""
print(ftable['the'])    # frequency count of the word 'the'    e.g. the -- 5580
print(ftable.N())       # returns total size of the sample (entire corpus)
print(ftable.freq('the'))   # returns frequency of occurrence of 'the' in corpus
"""

# 10 most frequent words in the corpus
wlist = list(ftable.keys())     # convert dict_keys to a list of tags
ten_common = ftable.most_common()[:10]

# print out a table of the words and their respective counts
#for(word, count) in ftable.most_common()[:10]:
#	print(count, word)

#ftable_horizontal = ftable.tabulate(10)

# return word with highest frequency
max_key = ftable.max()

# plot freq distribution, TODO install MatPlotLib
#plot = ftable.plot(25)
#plot_cumulative = ftable.plot(25, cumulative=True)

# frequency distribution of tags, using Universal Tagset (12 tags)
tagged_words = brown.tagged_words(categories="news", tagset="universal")
ttable = nltk.FreqDist()
for(word, tag) in tagged_words:
	ttable[tag] += 1
#print(list(ttable.keys()))

# top tags encountered
"""
for tag in ttable.keys():
	print(ttable[tag], tag)
"""

# compute the top 10 most frequent verbs
"""vtable = nltk.FreqDist()
for (word, tag) in tagged_words:
	if tag == 'VERB':
		vtable[word+"/"+tag] += 1
for (word_tag, count) in vtable.most_common()[:10]:
	print(count, word_tag)
"""



btw = brown.tagged_words(categories="news", tagset="universal")
bts = brown.tagged_sents(categories="news", tagset="universal")
bs = brown.sents(categories="news")

s = "A man, a plan , a canal Panama."

# NLTK Tokenizer
words = nltk.word_tokenize(s)
#print(words)

# NLTK Tagger with tokenized words
tagged = nltk.pos_tag(words, tagset="universal")
#print(tags)

# tag any given sentence
"""for sent in bs[:5]:
	print(nltk.pos_tag(sent))"""

# create list of all the tags, create freq table
tags = [tag for (word, tag) in btw]
tDist = nltk.FreqDist(tags)
for(word, count) in tDist.most_common()[:10]:
	print(count, word)

# DEFAULT TAGGER
# approximation tagger - assign every word NOUN
dTagr = nltk.DefaultTagger("NOUN")
n_tagged = dTagr.tag(words)
#print(n_tagged)

# evaluate the accuracy of the tagger
# #tags correctly assigned / #total # of tags  * 100
accuracy = 3/10
print(accuracy)

d_accuracy = dTagr.evaluate(bts)
print(d_accuracy)

# accuracy of dTagr for our sameple sent
d_sent_acc = dTagr.evaluate([nltk.pos_tag(words, tagset="universal")])	# 30%
print(d_sent_acc)


# REGEX TAGGER
patterns = [
 (r'[\.,:;\'"?!]', '.'),          # Punctuation
 (r'.*ing$', 'VERB'),             # gerunds
 (r'.*ed$', 'VERB'),              # simple past
 (r'.*es$', 'VERB'),              # 3rd singular present
 (r'.*ould$', 'VERB'),            # modals
 (r'.*\'s$', 'NOUN'),             # possesive nouns
 (r'.*s$', 'NOUN'),               # plural nouns
 (r'^-?[0-9]+(.[0-9]+)?$', 'NUM'),# cradinal numbers
 (r'.*', 'NOUN')                  # nouns (default)
 ]

reTagr = nltk.RegexpTagger(patterns)
reTagr.tag(bs[1011])
reTagr.evaluate(bts)		# 45%


# UNIGRAM TAGGER, supplied with gold standard to build internal model
uTagr = nltk.UnigramTagger(bts)
uTagr.evaluate(bts)			# 96.67%
# ==> training and testing on same data results in good performance... but usually
# taggers are trained on a subset of the corpus and then tested against unseen sentences
# e.g. train the tagger on 90% of the corpus, and then test it against the remaining 10%

N = int(len(bts) * 0.9)
train = bts[:N]
test = bts[N:]
uTagr = nltk.UnigramTagger(train)
uTagr.evaluate(test)		# 84.5%

# BIGRAM TAGGER
bTagr = nltk.BigramTagger(train)
bTagr.evaluate(test)		# 14.8%, so bad!

"""
so bad bc lots are assigned the "none" tag... bc it's a bigram, no prior instances present
that matched pair of words being considered. we can make this better using cascade
"""
# we can use a backup "backoff" tagger (default)
bdTagr = nltk.BigramTagger(train, backoff=dTagr)
bdTagr.evaluate(test)		# 87%

# unigram as backup
buTagr = nltk.BigramTagger(train, backoff=uTagr)
buTagr.evaluate(test)		# 85%

# cascade multiple taggers this way: NLTK documentation for other N-gram
# taggers and experiment to see how to achieve the maximum accuracy

# HMM TAGGER

from nltk.tag import hmm
hmmTagr = hmm.HiddenMarkovModelTagger.train(bts)
sentence = "A man, a plan, a canal Panama!"
# tokenize sent
tsent = nltk.word_tokenize(sentence)

# tag sent with hmmTagr
tagged_sent = hmmTagr.tag(tsent)
# eval on entire training set
hmmTagr.evaluate(bts)		# 97%

#eval on training & test data
N = int(len(bts)*0.9)
train = bts[:N]
test = bts[N:]

# train HMM tagger on training set
hmmTagr = hmm.HiddenMarkovModelTagger.train(train)
# tag a sentence with it
hmmTagr.tag(tsent)
# evaluate on test data
hmmTagr.evaluate(test)		# 88.7%
