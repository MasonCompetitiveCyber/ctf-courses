message = "there is no way that a bee should be able to fly"

special_chars = iter("~!@#$%^&*()-=+_[]{}<>?,.;:")

mapping = {}
for letter in message:
	if letter in mapping:
		continue
	elif letter == " ":
		continue
	else:
		mapping[letter] = next(special_chars)


secret = ""
for letter in message:
	if letter == " ":
		secret += " "
	else:
		secret += mapping[letter]

print(secret)

crazy = "".join([" " if letter == " " else mapping[letter] for letter in message])
print(crazy)