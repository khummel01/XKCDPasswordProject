from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
Bootstrap(app)

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

	# Letter to number dictionary
	letNumDict = {"c": "3", "i": "1", "g": "6", "b": "9", "o": "0", "h": "4", "e": "8"}

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

	if letNumSub == None and easyType == None or letNumSub == "on" and easyType == None:
		random.shuffle(correctLenRange)
		simplePasswords = []
		while len(simplePasswords) != 10:
			newPassword = ""
			# wordCount = 0
			for i in range(4):
				randoWord = random.choice(correctLenRange)
				if randoWord not in newPassword:
					newPassword += randoWord
					# wordCount += 1
			if newPassword not in simplePasswords and letNumSub == None and len(newPassword) <= maxOverAllLen:
				simplePasswords.append(newPassword)
			elif newPassword not in simplePasswords and letNumSub == "on":
				numSubPassword = ""
				for i in range(len(newPassword)):
					if newPassword[i] in letNumDict:
						numSubPassword += letNumDict[newPassword[i]]
					else:
						numSubPassword += newPassword[i]
				simplePasswords.append(numSubPassword)
		return render_template("passwords.html", passwordLst = simplePasswords)

	left  = "asdfgzxcvbqwertASDFGZXCVBQWERT"
	right = "jklhyuiopnmJKLHYUIOPNM"
	if letNumSub == None and easyType == "on" or letNumSub == "on" and easyType == "on":
		random.shuffle(correctLenRange)
		easyTypePasswords = []
		while len(easyTypePasswords) != 10:
			newPassword = ""
			place = None
			wordCount = 0
			while wordCount < 4:
				randoWord = random.choice(correctLenRange)
				if randoWord not in newPassword and place == None:
					newPassword += randoWord
					place = len(randoWord)-1
					wordCount += 1
				elif randoWord not in newPassword and place != None:
					## have to look at the last word!
					if randoWord[0] in left and newPassword[place] in right or randoWord[0] in right and newPassword[place] in left:
						newPassword += randoWord
						place += len(newPassword[place:])-1
						wordCount += 1
			if newPassword not in easyTypePasswords and letNumSub == None and len(newPassword) <= maxOverAllLen:
				easyTypePasswords.append(newPassword)
			elif newPassword not in easyTypePasswords and letNumSub == "on":
				numSubPassword = ""
				for i in range(len(newPassword)):
					if newPassword[i] in letNumDict:
						numSubPassword += letNumDict[newPassword[i]]
					else:
						numSubPassword += newPassword[i]
				easyTypePasswords.append(numSubPassword)
		return render_template("passwords.html", passwordLst = easyTypePasswords)

@app.route("/error")
def errorMessage():
	return render_template("error.html")


if __name__ == "__main__":
	app.run(debug=True)
