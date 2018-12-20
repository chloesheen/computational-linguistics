"""
Assignment 3: Hashtag Tokenizer
Chloe Sheen
"""
import nltk
import urllib.request

def max_match(hashtag, lexicon):
	"""max_match(hashtag, lexicon)
	   input: hashtag, lexicon
	   output: segment the input into tokens using an English dictionary and MaxMatch algorithm
	   ** Using pseudocode provided in Dan Jurafsky's Speech & language Processing
		  2.4.3 Word Segmentation in Chinese: the MaxMatch algorithm
	"""
	if not hashtag:
		result = []
		return result
	for i in range (len(hashtag)-1, -1, -1):
		first_word = hashtag[:i+1]              # first i chars of strings
		remainder = hashtag[i+1:len(hashtag)]   # rest of strings
		if first_word in lexicon:
			result = [first_word] + max_match(remainder, lexicon)
			max_match_result = []
			x_joined = ' '.join(result)
			max_match_result.append(x_joined)
			return max_match_result
	# otherwise, create a one-char word
	first_word = hashtag[0]                    # first char of string
	remainder = hashtag[1:len(hashtag)]        # rest of string
	result = [first_word] + max_match(remainder, lexicon)
	return result

def del_cost(source):
	return 1

def ins_cost(target):
	return 1

def sub_cost(source, target):
	if source == target:
		return 0
	else:
		return 2

def min_edit_distance(source, target):
	"""min_edit_distance(source, target)
	   input: source, target
	   output: minimum edit distance from source to target strings
	"""
	n = len(source)
	m = len(target)

	# creating a distance matrix
	distance = [[0 for x in range(n+1)] for y in range(m+1)]

	for i in range(1, m+1):
		distance[i][0] = distance[i-1][0] + ins_cost(target[i-1])
	for j in range(1, n+1):
		distance[0][j] = distance[0][j-1] + del_cost(source[j-1])
	for i in range(1, m+1):
		for j in range(1, n+1):
			distance[i][j] = min(distance[i-1][j] + 1,
								 distance[i][j-1] + 1,
								 distance[i-1][j-1] + sub_cost(source[j-1], target[i-1]))
	return distance[m][n]

def word_error_rate(guess, answer):
	"""word_error_rate(ref, hypo)
	   input: output from MaxMatch (guess), correct answers (answer)
	   output: length normalized minimum edit distance
				minimum edit distance divided by the length of the correct segmentation string
	"""
	distance = min_edit_distance(guess, answer)
	return 100 * float(distance) / len(answer)

if __name__ == '__main__':
	sample_hashtags = urllib.request.urlopen('https://cs.brynmawr.edu/Courses/cs325/fall2018/testHashtags.txt').read().decode()
	a_hashtag_lines = sample_hashtags.splitlines()
	hashtag_lines = []
	for x in a_hashtag_lines:
		x_joined = ''.join(x).strip(" ")      #bigbangtheory has an additional space at the end
		hashtag_lines.append(x_joined)

	NLTKdict = [word.lower() for word in nltk.corpus.words.words()]
	linux_dict = open('/usr/share/dict/words').read()
	linux_lines = [word.lower() for word in linux_dict.splitlines()]
	google_dict = urllib.request.urlopen('https://cs.brynmawr.edu/Courses/cs325/fall2018/bigWordList.txt').read().decode()
	google_lines = [word.lower() for word in google_dict.splitlines()]

	"""for i in range(len(hashtag_lines)):
		print(max_match(hashtag_lines[i], NLTKdict))
		print(max_match(hashtag_lines[i], linux_lines))
		print(max_match(hashtag_lines[i], google_lines))
	"""
	hashtag_answers = urllib.request.urlopen('https://cs.brynmawr.edu/Courses/cs325/fall2018/testWithAnswers.txt') \
											.read().decode()
	answers_lines = [word for word in hashtag_answers.splitlines()]
	hashtag_answers_list = []
	hashtag=[]
	answer_list=[]

	for answer in answers_lines:
		answer = answer.split(',')
		hashtag_answers_list.append(answer)

	for words in hashtag_answers_list:
		answer_list.append(words[1])

	for i in range(len(hashtag_lines)):
		max_result = max_match(hashtag_lines[i],NLTKdict)
		print("Expected Answer: " + answer_list[i])
		max_match_result = ' '.join(max_result)
		print("MaxMatch Answer: " + max_match_result)
		print("Word Error Rate: " , word_error_rate(max_match_result, answer_list[i]))
