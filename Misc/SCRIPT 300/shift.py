letters = list("its wings are too small to get its fat little body off the ground")

def shift(letter, shift=3):
	if letter == " ":
		return " "
	else:
		return (chr((ord(letter) + shift - 97) % 26 + 97))

shifted_list = list(map(shift, letters))
shifted = "".join(shifted_list)
print(shifted)

from itertools import repeat
shifted_list = list(map(shift, letters, repeat(5)))
shifted = "".join(shifted_list)
print(shifted)

shifted_list = list(map(lambda letter, shift: " " if letter == " " else (chr((ord(letter) + shift - 97) % 26 + 97)), letters, repeat(3)))
shifted = "".join(shifted_list)
print(shifted)