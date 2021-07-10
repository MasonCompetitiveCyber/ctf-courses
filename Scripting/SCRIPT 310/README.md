<h1 align="center">SCRIPT 310</h1>
  <p align="center">
     Python: Useful Libraries
  </p>

### Table of contents

- [Prerequisites](#prerequisites)
- [Introduction](#introduction)
- [General](#general)
  - [string](#string)
  - [pprint](#pprint)
- [Data Conversion](#data-conversion)
  - [base64](#base64)
  - [binascii](#binascii)
  - [`bytes.hex()` and `bytes.fromhex()`](#byteshex-and-bytesfromhex)
- [Example CTF Problem](#example-ctf-problem)
- [Next Steps](#next-steps)
- [More Resources](#more-resources)
- [Creators](#creators)

## Prerequisites
- Scripting 200
  - You should be comfortable with basic python programming (if/else, loops, functions)
- Scripting 300
  - You should be comfortable with using some more advanced python functions

## Introduction
This course will introduce you to various Python libraries that will greatly assistyou in solving CTF challenges (and are generally useful as well). 


## General
### string
The `string` library is pretty sweet. It gives us quick access to strings containg numbers, lowecase and uppercase letters, and several more. Here's an example:

```python
>>> import string
>>> string.ascii_letters
'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> string.whitespace
' \t\n\r\x0b\x0c'
>>> string.punctuation
'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
>>> string. # the below output is some autocomplete suggestions of string methods
┌─────────────────────────────────────────────────────────────────────────────────┐
│ Formatter              Template               ascii_letters                     │
│ ascii_lowercase        ascii_uppercase        capwords                          │
│ digits                 hexdigits              octdigits                         │
│ printable              punctuation            whitespace                        │
└─────────────────────────────────────────────────────────────────────────────────┘
```
One quick example of where you could use this is to clean some data. Let's say we were given the following data: 
```
t!"he#$ b%&ee'( o)*f +,co-.ur/:se;< f=>li?@es[\ a]^ny_`wa{|y }~be!"ca#$us%&e '(be)*es+, d-.on/:t ;<ca=>re?@ w[\ha]^t _`hu{|ma}~ns!" t#$hi%&nk'( i)*s +,im-.po/:ss;<ib=>le?@
```
If we wanted to get rid of all of the special characters/punctuation, we could do so with the following script ([clean.py]((https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Scripting/SCRIPT%20310/clean.py)):
```python
import string

text = """t!"he#$ b%&ee'( o)*f +,co-.ur/:se;< f=>li?@es[\ a]^ny_`wa{|y }~be!"ca#$us%&e '(be)*es+, d-.on/:t ;<ca=>re?@ w[\ha]^t _`hu{|ma}~ns!" t#$hi%&nk'( i)*s +,im-.po/:ss;<ib=>le?@"""

output = ""
for c in text:
	if c not in string.punctuation:
		output += c

print(output)
---------------------------------------------------
output: the bee of course flies anyway because bees dont care what humans think is impossible
```
You can see that we use `string.punctuation` for quick access to a string containing all punctuation instead of having to create on manually. 

### pprint
`pprint` is another quick and easy library to make our lives a little better. `pprint` stands for pretty print, so you can image what this does:
```python
>>> from pprint import pprint
>>> dic = {40: 'yellow', 39: 'black', 38: 'yellow', 37: 'black', 36: 'yellow', 35: 'black', 34: 'yellow'
, 33: 'black', 32: 'ooh', 31: 'black', 30: 'and', 29: 'yellow'}
>>> print(dic)
{40: 'yellow', 39: 'black', 38: 'yellow', 37: 'black', 36: 'yellow', 35: 'black', 34: 'yellow', 33: 'bla
ck', 32: 'ooh', 31: 'black', 30: 'and', 29: 'yellow'}
>>> pprint(dic)
{29: 'yellow',
 30: 'and',
 31: 'black',
 32: 'ooh',
 33: 'black',
 34: 'yellow',
 35: 'black',
 36: 'yellow',
 37: 'black',
 38: 'yellow',
 39: 'black',
 40: 'yellow'}
>>> pprint(dic, sort_dicts=False)
{40: 'yellow',
 39: 'black',
 38: 'yellow',
 37: 'black',
 36: 'yellow',
 35: 'black',
 34: 'yellow',
 33: 'black',
 32: 'ooh',
 31: 'black',
 30: 'and',
 29: 'yellow'}
```
It just prints out our data nicely. It has a default setting to sort dictionaries, but you can turn that off if you want to. Cool.

## Data Conversion
### base64
Base64 is a popular encoding mechansim you'll encounter in the real world and CTFs, so it's good to know how to encode and decode from it. There are many tools online that can do it for you, such as:
- https://www.base64decode.org/
- https://codebeautify.org/base64-decode
- http://icyberchef.com/

This being said, you'll probably find yourself needing to do this in a script. `base64` makes it super easy:
```python
>>> import base64
>>> base64.b64encode("Let's shake it up a little.")
Traceback (most recent call last):
  File "<input>", line 1, in <module>
    base64.b64encode("Let's shake it up a little.")
  File "/usr/lib/python3.9/base64.py", line 58, in b64encode
    encoded = binascii.b2a_base64(s, newline=False)
TypeError: a bytes-like object is required, not 'str'

>>> base64.b64encode(b"Let's shake it up a little.")
b'TGV0J3Mgc2hha2UgaXQgdXAgYSBsaXR0bGUu'
>>> base64.b64encode(("Let's shake it up a little.").encode("utf-8"))
b'TGV0J3Mgc2hha2UgaXQgdXAgYSBsaXR0bGUu'

>>> base64.b64decode(b'TGV0J3Mgc2hha2UgaXQgdXAgYSBsaXR0bGUu')
b"Let's shake it up a little."
>>> base64.b64decode(b'TGV0J3Mgc2hha2UgaXQgdXAgYSBsaXR0bGUu').decode("utf-8")
"Let's shake it up a little."
```
We can see that at first, I got an error trying to b64encode a string, as it requires a byte-like object instead of a string. We can do this a couple ways. One way is to prepend the string denoted by `" "` with a *b*, so `b" "`. This tells python that this is a byte object. Strings also have `decode()` and `encode()` functions. `encode()` allows the conversion between strings of a specified encoding (default is UTF-8) to bytes. `decode()` will do the opposite. After converting our string to bytes, we see that `b64encode()` converts our string to base64. We can then also decode that string if passed in as bytes. By default, it will spit out bytes back to us, but we can use `decode()` to convert it to a normal string. 

### binascii
Converting between hex and ascii is also very useful in many situations since you'll find a lot of data stored as hex (like hexdumps of files). Luckily, `binascii` has two nice methods called `hexlify()` and `unhexlify()` to simplify this for us. Let's take a look:
```python
>>> import binascii
>>> binascii.hexlify(b'Barry! Breakfast is ready!')
b'42617272792120427265616b6661737420697320726561647921'
>>> binascii.unhexlify(b'42617272792120427265616b6661737420697320726561647921')
b'Barry! Breakfast is ready!'
```
As you can see, these functions go through every byte of the input and convert it to hex or vice-versa. It will output in bytes, so remember that you might need to decode those into strings if you want to run string functions on them. 

### `bytes.hex()` and `bytes.fromhex()` 
After writing the last section I realized there is also a built-in function that does basically the same thing, lol. I guess it's up to preference (binasciihas some other useful methods too).
```python
>>> bytes.hex(b'Barry! Breakfast is ready!')
'42617272792120427265616b6661737420697320726561647921'
>>> bytes.fromhex('42617272792120427265616b6661737420697320726561647921')
b'Barry! Breakfast is ready!'
```
Notice that there is a slight difference, `bytes.hex()` outputs a string and not a bytes object like `binascii.hexlify()`. 

## Example CTF Problem
Let's say we are given the following file [flag.txt]((https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Scripting/SCRIPT%20310/flag.txt). If you open it, it looks completely empty. Let's use a linux tool called `hexdump` to see the raw data:
```console
$ hexdump flag.txt  
0000000 0d0a 0a0d 0d0a 0a0d 0d0a 0a0d 0d0d 0a0a
0000010 0d0a 0a0d 0a0a 0d0a 0d0a 0a0d 0d0a 0d0d
0000020 0d0a 0d0d 0a0d 0d0d 0d0a 0a0d 0a0d 0a0a
0000030 0d0a 0a0d 0a0a 0d0a 0d0a 0a0d 0d0d 0a0a
0000040 0d0a 0a0d 0d0a 0a0d 0d0a 0d0a 0d0d 0d0d
0000050 0d0a 0a0d 0a0a 0d0a 0d0a 0d0a 0d0d 0d0d
0000060 0d0a 0a0d 0a0a 0a0d 0d0a 0d0d 0a0d 0d0a
0000070 0d0a 0d0d 0d0a 0a0a 0d0a 0a0d 0d0a 0d0a
0000080 0d0a 0d0a 0d0d 0d0d 0d0a 0a0d 0a0d 0d0a
0000090 0d0a 0d0d 0a0a 0d0d 0d0a 0d0a 0d0d 0d0d
00000a0 0d0a 0a0d 0a0a 0d0d 0d0a 0a0d 0a0a 0d0a
00000b0 0d0a 0a0d 0d0d 0a0a 0d0a 0a0d 0d0d 0a0a
00000c0 0d0a 0a0d 0d0a 0d0a 0d0a 0a0d 0d0a 0a0a
00000d0 0d0a 0d0a 0d0d 0d0d 0d0a 0a0d 0a0a 0d0a
00000e0 0d0a 0d0a 0d0d 0d0d 0d0a 0a0d 0d0d 0a0d
00000f0 0d0a 0a0d 0a0d 0d0a 0d0a 0a0d 0a0a 0a0d
0000100 0d0a 0a0d 0a0a 0a0d 0d0a 0a0d 0d0d 0a0a
0000110 0d0a 0a0d 0d0a 0d0a 0d0a 0d0d 0d0d 0d0a
```
Well, it looks like it's not empty after all, rather filled with `0a` and `0d`. Looking at https://www.asciitable.com/, we see that `0a` represents a new line and `0d` represents carriage return. You can read about these online and their differnces, but they're basically characters denoting new lines. Now it should make sense why the file looked empty. Since these are the only two values in the file, we can make the assumption that it might be some sort of binary data, 1s and 0s, just reperesnted as `0a` and `0d` (usually you won't just figure out what is going on instantaneosly when looking at a challenge, but since I know the solution, that's why it seems so easy). Let's try to convert this data to 1s and 0s and then see what we get. Here's the python script:
```python
import binascii

f = open('flag.txt', 'rb')

content = f.read()
print(f"Content: {content}")
print("-----------------------")

hex_flag = binascii.hexlify(content).decode()
print(f"Hex: {hex_flag}")
print("-----------------------")

binary = hex_flag.replace('0a', '0').replace('0d', '1')
print(f"Binary: {binary}")
print("-----------------------")

# convert every 8 bits (1 byte) into a character
characters = []
for i in range(len(binary)//8): 
    bin2int = int(binary[ i*8 : i*8+8 ], 2)
    int2char = chr(bin2int)
    characters.append(int2char)
print(f"List of characters: {characters}")
print("-----------------------")

flag = "".join(characters)
 
print(flag)
```
We start by opening the file and using `rb` to read the content of the file in bytes. We then take those bytes and convert them to hex, which should turn them into the `0a`'s and `0d`'s we saw from the hexdump. We can then replace the `0a` with a 0 and the `0d` with a 1 (this is just a guess for now, we can switch them if it doesn't work out). Once we have our 1s and 0s, we need to convert that to normal ascii text, which we do in the for loop. For every 8 bits, we convert the byte into an integer, then that integer into a character, and append it to a list. Finally we join the list and print out our result. Here's the output to the script [solve.py]((https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Scripting/SCRIPT%20310/solve.py):
```console
$ python3 solve.py
Content: b'\n\r\r\n\n\r\r\n\n\r\r\n\r\r\n\n\n\r\r\n\n\n\n\r\n\r\r\n\n\r\r\r\n\r\r\r\r\n\r\r\n\r\r\n\r\n\n\n\n\r\r\n\n\n\n\r\n\r\r\n\r\r\n\n\n\r\r\n\n\r\r\n\n\r\n\r\r\r\r\r\n\r\r\n\n\n\n\r\n\r\n\r\r\r\r\r\n\r\r\n\n\n\r\n\n\r\r\r\r\n\n\r\n\r\r\r\n\r\n\n\n\r\r\n\n\r\n\r\n\r\n\r\r\r\r\r\n\r\r\n\r\n\n\r\n\r\r\r\n\n\r\r\n\r\n\r\r\r\r\r\n\r\r\n\n\n\r\r\n\r\r\n\n\n\n\r\n\r\r\n\r\r\n\n\n\r\r\n\r\r\n\n\n\r\r\n\n\r\n\r\n\r\r\n\n\r\n\n\n\r\n\r\r\r\r\r\n\r\r\n\n\n\n\r\n\r\n\r\r\r\r\r\n\r\r\n\r\r\r\n\n\r\r\n\r\n\n\r\n\r\r\n\n\n\r\n\n\r\r\n\n\n\r\n\n\r\r\n\r\r\n\n\n\r\r\n\n\r\n\r\n\r\r\r\r\r\n\r'
-----------------------
Hex: 0a0d0d0a0a0d0d0a0a0d0d0a0d0d0a0a0a0d0d0a0a0a0a0d0a0d0d0a0a0d0d0d0a0d0d0d0d0a0d0d0a0d0d0a0d0a0a0a0a0d0d0a0a0a0a0d0a0d0d0a0d0d0a0a0a0d0d0a0a0d0d0a0a0d0a0d0d0d0d0d0a0d0d0a0a0a0a0d0a0d0a0d0d0d0d0d0a0d0d0a0a0a0d0a0a0d0d0d0d0a0a0d0a0d0d0d0a0d0a0a0a0d0d0a0a0d0a0d0a0d0a0d0d0d0d0d0a0d0d0a0d0a0a0d0a0d0d0d0a0a0d0d0a0d0a0d0d0d0d0d0a0d0d0a0a0a0d0d0a0d0d0a0a0a0a0d0a0d0d0a0d0d0a0a0a0d0d0a0d0d0a0a0a0d0d0a0a0d0a0d0a0d0d0a0a0d0a0a0a0d0a0d0d0d0d0d0a0d0d0a0a0a0a0d0a0d0a0d0d0d0d0d0a0d0d0a0d0d0d0a0a0d0d0a0d0a0a0d0a0d0d0a0a0a0d0a0a0d0d0a0a0a0d0a0a0d0d0a0d0d0a0a0a0d0d0a0a0d0a0d0a0d0d0d0d0d0a0d
-----------------------
Binary: 011001100110110001100001011001110111101101101000011000010110110001100110010111110110000101011111011000100111100101110100011001010101111101101001011100110101111101100011011000010110110001101100011001010110010001011111011000010101111101101110011010010110001001100010011011000110010101111101
-----------------------
List of characters: ['f', 'l', 'a', 'g', '{', 'h', 'a', 'l', 'f', '_', 'a', '_', 'b', 'y', 't', 'e', '_', 'i', 's', '_', 'c', 'a', 'l', 'l', 'e', 'd', '_', 'a', '_', 'n', 'i', 'b', 'b', 'l', 'e', '}']
-----------------------
flag{half_a_byte_is_called_a_nibble}
```
Hopefully that output helps you visualize each step of the process. You might notice the "Content" output is all `\n` and `\r`. `\n` is the newline character and `\r` is the carriage return. Anyways, we got the flag, yay!

*CTF challenge based off of RADAR CTF 2019 – Blanks, with writeup from https://ironhackers.es/en/writeups/resolviendo-retos-de-ctf-parte-1/*

*p.s. You can use online tools to help with conversions too, like https://www.rapidtables.com/convert/number/binary-to-ascii.html to convert the binary to ascii*

## Next Steps
 - make [solve.py]((https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Scripting/SCRIPT%20310/solve.py) in less lines of code (using string comprehension and stuff)
- create the inverse of [solve.py]((https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Scripting/SCRIPT%20310/solve.py), a.k.a a script that creates and empty looking file from a string 

## More Resources
- https://www.kite.com/python/docs/binascii.hexlify
- https://stackoverflow.com/questions/6624453/whats-the-correct-way-to-convert-bytes-to-a-hex-string-in-python-3

## Creators

**Daniel Getter**

Enjoy :metal: