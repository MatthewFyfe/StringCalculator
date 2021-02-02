#Technical Interview - String Calculator
# Matthew Fyfe, Feb 2021

##############################################################################

# Bonus 4: using regular expressions makes multi-delimiter case easier
import re

# Part 1: simple string calculator
def Add(numbers: str):
	'''Add together a string of delimiter separated integers.

	Takes in an string of delimiter separated numbers. Adds them together.
	This program naively assumes the input is in the correct format.
	Ex input: '1,2,3' or '//;\n1;3;4'

	:param str numbers: a delimiter separated string of integers
	:raise: Exception if one of the integers < 0
	:return: an integer value represetning the sum of the inputs
	:rtype: int
	'''

	multiDelim_flag = False

	# Part 1: check for empty string
	if not numbers:
		return 0
	
	# Part 3: Check for custom delimiter
	numbers = extractCustomDelimter(numbers)
	# We expect a tuple if there was a custom delimiter
	if (type(numbers) is tuple):
		delimiter = numbers[1]
		numbers = numbers[0]

		# Bonus 3: handle multi delimter case
		if(type(delimiter) is list):
			delimiterString = ""
			
			for x in delimiter:
				# TODO: should insert escape characters into x to handle '$$' case
				# Just handling naive case for now (put a \ at start)
				delimiterString += '\\' +str(x) + '|'

			# Remove the last '|'
			delimiterString = delimiterString[:-1]
			multiDelim_flag = True
	# Part 1: Default to ',' if not custom
	else:
		delimiter = ','

	# Part 2: Handle new line characters
	numbers = removeNewLines(numbers)

	# Part 1: Split the delimter seperated values (, if not specified)
	# Use map to cast each value into integers, then sum the values
	# Part 4: Also verify there are no negatives numbers in the input
	# Note: must save map results as list, otherwise it expires after single use
	if(not multiDelim_flag):
		result = list(map(int, numbers.split(delimiter)))
	else:
		result = list(map(int, re.split(delimiterString, numbers)))

	# Bonus 1: ignore large numbers
	result = sum(ignoreTooBig(noNegatives(result)))

	# Part 1: return integer result
	return result;


# Part 2: handle new line characters in the input string
def removeNewLines(text: str):
	''' Strip out newline characters from a string

	:param str text: the input text to be modified
	:return: the modified string without newline characters
	:rtype: str
	'''

	return text.replace('\n', '')


# Part 3: support custom delimiter
def extractCustomDelimter(text: str):
	''' Check for and identify the custom delimiter

	:param str text: input string to be scanned for delimters
	:return: a tuple containing both the input text without the delimiter
	code and the extracted delimiters
	:rtype: tuple
	'''

	#check for // code, if we don't find one assume this is a non-custom case
	if(text.find('//') != 0):
		return text

	#extract delimter...
	#expected format: “//[delimiter]\n[delimiter separated numbers]”
	firstPosition = text.find('//')
	secondPosition = text.find('\n')

	delimiter = text[firstPosition+2:secondPosition]

	#extract input text
	trimmedText = text[secondPosition::]

	#return delimiter and trimmed numbers text as tuple
	# Bonus 3: check for multiple delimiters
	# Assume ',' is always the delimiter delimiter :)
	multiDelimiter = delimiter.split(',')
	if(len(multiDelimiter) > 1):
		return(trimmedText, multiDelimiter)
	else:
		return(trimmedText, delimiter)


# Part 4: check for negative numbers
def noNegatives(numbers: list):
	''' Check the input list for negatives numbers, throw exception if found.

	:param list numbers: the input list to be scanned
	:raise: Exception if a negative number is found
	:return: the unmodified list from our input
	:rtype: list
	'''

	negativesList = []

	for x in numbers:
		if x < 0:
			negativesList.append(x)

	# Raise an exception if we found any negative numbers in the input
	if(len(negativesList) > 0):
		raise Exception("Negatives not allowed" + str(negativesList))

	# Otherwise, just return the values
	return numbers


# Bonus 1: ignore numbers larger than 1000 from input
def ignoreTooBig(numbers: list):
	''' Set values > 1000 to 0 so that they are ignored during sum.

	:param list numbers: the input list to be scanned
	:return: the potentially modified list from our input
	:rtype: list
	'''

	tooBigList = []

	# Find values over 1000
	for x in numbers:
		if x > 1000:
			tooBigList.append(x)

	# Remove the bad values from our input list
	for y in tooBigList:
		numbers.remove(y)

	return numbers

##############################################################################

# Run the tests for the program

#Part 1
print("1,2,5 = " + str(Add("1,2,5")))
print("[empty_string] = " + str(Add("")))

#Part 2 
print("1\\n,2,3 = " + str(Add("1\n,2,3")))
print("1,\\n2,4 = " + str(Add("1,\n2,4")))

#Part 3
print("//;\\n1;3;4 = " + str(Add("//;\n1;3;4")))

#Part 4 (causes exception, as intended)
#print("// \n1 -2 -3 = " + str(Add("// \n1 -2 -3")))

#Bonus 1
print("2,1001 = " + str(Add("2,1001")))

#Bonus 2
print("//***\\n1***2***3 = " + str(Add("//***\n1***2***3")))

#Bonus 3
print("//$,@\\n1$2@3 = " + str(Add("//$,@\n1$2@3")))

#Bonus 4 (with limitation, dont use multiple characters that must be escaped)
print("//$ ,@\\n4$ 2@3 = " + str(Add("//$ ,@\n4$ 2@3")))

