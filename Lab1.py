"""
Chloe Sheen
CS 325: Assignment 1
"""
import nltk
from nltk.book import *
import urllib.request
import re

def lexical_diversity(text):
	"""lexical_diversity(text)
	   input: text
	   output: lexical diversity, the # tokens in text / vocabulary of text
	"""
	return len(text) / len(set(text))

def percentage_use(word, words):
	"""percentage_use(word, words)
	   input: word to search for, text of words
	   output: percentage use of given word in a text (words)
	"""
	return 100 * (words.count(word)/len(words))

def prefix_search(prefix):
	"""prefix_search(prefix)
	   input: prefix
	   output: tuple, returns a list of the first 20
			   words that begin with prefix & the number of those words
	"""
	wordlist = nltk.corpus.words.words("en")
	result = [word for word in wordlist if re.match(prefix, word)]
	return result[:20], len(result)

def office_hours(url):
	"""office_hours(url)
	   input: url
	   output: extract and print office hours of instructor from CS325 page
	"""
	page = urllib.request.urlopen(url).read().decode()
	#result = re.search(r'</strong>(.+?)<br\sclear="ALL">', page)
	general_result = re.search(r'[oO]ffice\s[hH]ours.*(\b\w{3,6}days?.*\d(\d)?:\d\d.*(?=<))', page)
	return general_result.group(1)

def weather_extract(url):
	"""weather_extract(url)
	   input: url
	   output: extract and print the current weather conditions &
			   temperature in Philadelphia from NOAA's weather server
	"""
	page = urllib.request.urlopen(url).read().decode()
	result = re.search(r"<weather>(.+?)(?=</weather>)", page)
	return result.group(1)

if __name__ == "__main__":
	"""
	print("\nLexical Diversity")
	for test_text in [text2, text4, text5, text6]:
		print(test_text, ": ", lexical_diversity(test_text), sep='')

	print("\nPercentage Use")
	test_word = "the"
	for test_text in [text2, text4, text5, text6]:
		print(test_text, " percentage of the word '",test_word, "': ",
			  percentage_use(test_word, test_text), sep='')
	"""
	#print("\nPrefix Search \n", prefix_search(r"\b[uU]n.+"))

	print("\nOffice Hours \n", office_hours("https://cs.brynmawr.edu/Courses/cs325/fall2018/"))

	#print("\nWeather \n", weather_extract("https://w1.weather.gov/xml/current_obs/display.php?stid=KPHL"))
