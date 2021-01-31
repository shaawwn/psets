import time
import string
import re
import math
import sys
# Create the cs50 spell checker pset using python using different search algorithms
	# to check the spelling

#---------------- ---------------Functions ----------------------------

# Create the dictionary
def create_dictionary(file):
	"""Open the given file and create an alphabetical dictionary
	putting each word in the appropriate alphabetic key-value comb.
	"""
	# Create the dictionary
	dictionary = {}
	alpha_keys = "abcdefghijklmnopqrstuvwxyz"

	for char in alpha_keys:
		dictionary[char] = []

	with open(file, "r") as f:
		lines = f.readlines()
		for line in lines:
			dictionary[line[0].lower()].append(line.strip())
	return dictionary


def size(dictionary):
	"""Return the int size number of words in a dictionary"""
	words = 0
	for values in dictionary.values():
		words += len(values)
	return words


def load_text(file):
	"""Load a text into a list"""
	text = []
	punc = string.punctuation
	puncRegex = re.compile(r"[\w]")
	with open(file, "r") as f:
		lines = f.readlines()
		for line in lines:
			line = line.split()
			for word in line:
				if word.isnumeric() == True: # Pass over numbers
					# print("Pass", word)
					pass
				word = puncRegex.findall(word.strip())
				if word == []:
					pass
				else:
					text.append("".join(word))
	f.close()
	return text




# ------------------------------   Spell checkers -----------------------------

# Python built-in search
def check_spelling(word, dictionary): # Linear search
	"""Check the spelling of a word by using Python's build in 'if in' function
	"""
	try:
		if word.lower() in dictionary.get(word[0].lower()):
			return True
	except TypeError: # Numbers were counting against misspellings, so just pass over them
		# print(word)
		pass
	else:
		# print(word)
		return False


def check_text(text, dictionary):
	"""Spell check an entire text with a given dictionary
	and give the run time
	"""
	start = time.time()
	misspelled_words = 0
	misspelled_list = []
	for word in text:
		# If a word is not spelled correctly by the dictionary, return False
		if check_spelling(word, dictionary) == False:
			# print(word)
			misspelled_list.append(word)
			misspelled_words += 1
	print("Number of misspelled words: ", misspelled_words)
	end = time.time()
	print("Time to execute Python's build in search", end - start, "\n")
	return misspelled_list





# Linear search ("Linear search"), I'm pretty sure this implementation at least is exponential
def linear_spelling(word, dictionary):
	"""Implement a linear search for the word from the text's spelling
	in the dictionary
	"""
	misspelled_words = 0
	misspelled_list = []
	try:
		for correct_word in dictionary.get(word[0].lower()):
			if correct_word == word.lower():
				return True
	# Don't include numbers
	except TypeError:
		pass
	else:
		return False


def linear_check_text(text, dictionary):
	"""Spell check an entire text with a given dictionary
	and give the run time
	"""
	start = time.time()
	misspelled_words = 0
	for word in text:
		if linear_spelling(word, dictionary) == False:
			misspelled_words += 1
	end = time.time()
	print("Number of misspelled words: ", misspelled_words)
	print("Time to execute linear search: ", end - start, "\n")
	return misspelled_list


# Binary Search
def binary_spelling(word, dictionary):
	"""Do a binary search for a word in a dictionary"""
	d = dictionary.get(word[0].lower())
	start = 0
	end = len(d) - 1
	mid = (start + end) // 2
	found = False
	while start <= end:
		mid = (start + end) // 2
		if d[mid] == word:
			# print("Found!", word)
			return True
		elif d[mid] > word:
			end = mid - 1

		elif d[mid] < word:
			start = mid + 1
	return False


def binary_check_text(text, dictionary):
	"""Spell check an entire text with a given dictionary
	and give the run time
	"""
	start = time.time()
	misspelled_words = 0
	misspelled_list = []

	for word in text:
		try:
			if binary_spelling(word.lower(), dictionary) == False:
				misspelled_list.append(word)
				misspelled_words += 1
		# Exclude numbers
		except TypeError:
			continue
	print("Number of misspelled words: ", misspelled_words)
	end = time.time()
	print("Time to execute binary search: ", end - start, "\n")
	return misspelled_list


# Jump Search
def jump_search(word, dictionary):
	"""Use a jump search to check the spelling of a word against the dictionary"""
	length = len(dictionary)
	jump = int(math.sqrt(length))
	left, right = 0, 0
	while left < length and dictionary[left] <= word:
		right = min(length - 1, left + jump)
		if dictionary[left] <= word and dictionary[right] >= word:
			break
		left += jump
	if left >= length or dictionary[left] > word:
		return False
	right = min(length - 1, right)
	i = left
	while i <= right and dictionary[i] <= word:
		if dictionary[i] == word:
			return True
		i += 1
	return False


def check_jump_search(text, dictionary):
	"""Spell check an entire text with a given dictionary
	and give the run time
	"""
	start = time.time()
	misspelled_words = 0
	misspelled_list = []
	for word in text:
		try:
		# If a word is not spelled correctly by the dictionary, return False
			if jump_search(word.lower(), dictionary.get(word[0].lower())) == False:
				misspelled_words += 1
		except TypeError:
			continue
	print("Number of misspelled words: ", misspelled_words)
	end = time.time()
	print("Time to execute Jump Search in search", end - start, "\n")
	return misspelled_list





# -------------------------- TESTING -------------------------------
# Load a dictionary and text in manually
# dictionary = create_dictionary('large')
# text = load_text('holmes.txt')


# Load dictionary/text via command line arguments
dictionary = create_dictionary(sys.argv[1])
text = load_text(sys.argv[2])

"""Test the actual algorthims"""
# linear_check_text(text, dictionary) #"linear"
check_text(text, dictionary)
binary_check_text(text, dictionary)
check_jump_search(text, dictionary)

