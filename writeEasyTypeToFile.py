with open("data/words.txt", "r") as infile:
    data = infile.read().splitlines()

left  = "asdfgzxcvbqwertASDFGZXCVBQWERT"
right = "jklhyuiopnmJKLHYUIOPNM"
with open("easyToTypeWords.txt", "w") as outfile:
    easyTypePasswords = []
    for word in data:
        for letter in word:
            easyTypeCount = 0
            if word[0] in left:
                for i in range(len(word)):
                    if i%2 != 0 and word[i] in right:
                        easyTypeCount += 1
                    elif i%2 == 0 and word[i] in left:
                        easyTypeCount += 1
                    else:
                        break
            else:
                for i in range(len(word)):
                    if i%2 != 0 and word[i] in left:
                        easyTypeCount += 1
                    elif i%2 == 0 and word[i] in right:
                        easyTypeCount += 1
                    else:
                        break

        if easyTypeCount == len(word):
            outfile.write(word + "\n")
