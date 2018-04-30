from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
Bootstrap(app)

def getNumSubPassword(newPassword):
	# Letter to number dictionary
	letNumDict = {"c": "3", "i": "8", "g": "5", "b": "2", "o": "0", "h": "7", "e": "1"}
	numSubPassword = ""
	for i in range(len(newPassword)):
		if newPassword[i] in letNumDict:
			numSubPassword += letNumDict[newPassword[i]]
		else:
			numSubPassword += newPassword[i]
	return numSubPassword

def getEasyTypePassword(correctLenRange, isNumSub):
	# characters in left and right hands for easy typing
	left  = "asdfgzxcvbqwertASDFGZXCVBQWERT12345"
	right = "jklhyuiopnmJKLHYUIOPNM67890"
	newPassword = ""
	place = None
	wordCount = 0
	while wordCount < 4:
		randoWord = random.choice(correctLenRange)
		if isNumSub:
			randoWord = getNumSubPassword(randoWord)
		if place == None:
			newPassword += randoWord
			place = len(randoWord)-1
			wordCount += 1
		if place != None:
			if randoWord[0] in left and newPassword[place] in right or randoWord[0] in right and newPassword[place] in left:
				newPassword += randoWord
				place += len(newPassword[place:])-1
				wordCount += 1
	return newPassword

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/passwords")
def generatePasswords():
	minLen = int(request.args.get("minSWLen"))
	maxLen = int(request.args.get("maxSWLen"))
	maxOverAllLen = int(request.args.get("maxOverAll"))
	letNumSub = request.args.get("letNumSub")
	easyType = request.args.get("easyTyping")

	# Check for any errors on the form
	if minLen > maxLen or minLen == 0 or maxLen == 0 or maxOverAllLen == 0 or maxLen > maxOverAllLen or minLen*4 > maxOverAllLen:
		return render_template("error.html")

	# Read in words.txt file
	with open("data/words.txt", "r") as file:
		regWords = file.read().splitlines()

	# Read in easyToTypeWords.txt
	with open("data/easyToTypeWords.txt", "r") as anotherFile:
		easyTypeWords = anotherFile.read().splitlines()

	# Get words with the correct length
	correctLenRange = []
	if easyType == "on":
		for word in easyTypeWords:
			if len(word) >= minLen and len(word) <= maxLen:
				correctLenRange.append(word)
	else:
		for word in regWords:
			if len(word) >= minLen and len(word) <= maxLen:
				correctLenRange.append(word)

	if letNumSub == None and easyType == None:
		random.shuffle(correctLenRange)
		simplePasswords = []
		while len(simplePasswords) != 10:
			newPassword = ""
			for i in range(4):
				randoWord = random.choice(correctLenRange)
				newPassword += randoWord
			if newPassword not in simplePasswords and len(newPassword) <= maxOverAllLen:
				simplePasswords.append(newPassword)
		return render_template("passwords.html", passwordLst = simplePasswords)

	if letNumSub == "on" and easyType == None:
		random.shuffle(correctLenRange)
		simpleNumPasswords = []
		while len(simpleNumPasswords) != 10:
			newPassword = ""
			for i in range(4):
				randoWord = random.choice(correctLenRange)
				if randoWord not in newPassword:
					newPassword += randoWord
			if newPassword not in simpleNumPasswords and len(newPassword) <= maxOverAllLen:
				simpleNumPasswords.append(getNumSubPassword(newPassword))
		return render_template("passwords.html", passwordLst = simpleNumPasswords)

	if letNumSub == None and easyType == "on":
		random.shuffle(correctLenRange)
		easyTypePasswords = []
		while len(easyTypePasswords) != 10:
			newPassword = getEasyTypePassword(correctLenRange, isNumSub = False)
			if newPassword not in easyTypePasswords and len(newPassword) <= maxOverAllLen:
				easyTypePasswords.append(newPassword)
		return render_template("passwords.html", passwordLst = easyTypePasswords)

	if letNumSub == "on" and easyType == "on":
		random.shuffle(correctLenRange)
		easyTypeNumPasswords = []
		while len(easyTypeNumPasswords) != 10:
			newPassword = getEasyTypePassword(correctLenRange, isNumSub = True)
			if newPassword not in easyTypeNumPasswords and len(newPassword) <= maxOverAllLen:
				easyTypeNumPasswords.append(newPassword)
		return render_template("passwords.html", passwordLst = easyTypeNumPasswords)

@app.route("/error")
def errorMessage():
	return render_template("error.html")


if __name__ == "__main__":
	app.run(debug=True)
