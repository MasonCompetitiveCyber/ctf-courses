import string

text = """t!"he#$ b%&ee'( o)*f +,co-.ur/:se;< f=>li?@es[\ a]^ny_`wa{|y }~be!"ca#$us%&e '(be)*es+, d-.on/:t ;<ca=>re?@ w[\ha]^t _`hu{|ma}~ns!" t#$hi%&nk'( i)*s +,im-.po/:ss;<ib=>le?@"""

output = ""
for c in text:
	if c not in string.punctuation:
		output += c

print(output)