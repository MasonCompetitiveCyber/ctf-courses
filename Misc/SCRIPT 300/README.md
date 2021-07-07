<h1 align="center">SCRIPT 300</h1>
  <p align="center">
     Python: Useful Built-in Functions
  </p>

### Table of contents

- [Prerequisites](#prerequisites)
- [Introduction](#introduction)
- [Useful Functions](#useful-functions)
	- [`enumerate()`](#enumerate)
	- [f-string](#f-string)
	- [`list()`](#list)
	- [`iter()` and `next()`](#iter-and-next)
	- [`.join()`](#join)
	- [List Comprehension](#list-comprehension)
	- [`ord()`, `chr()`, and `hex()`](#ord-chr-and-hex)
	- [`map()`](#map)
	- [Lambda Functions](#lambda-functions)
- [Next Steps](#next-steps)
- [More Resources](#more-resources)
- [Creators](#creators)

## Prerequisites
- Scripting 200
    - You should be comfortable with basic python programming (if/else, loops, functions)

## Introduction
This course will teach you useful and powerful Python built-in functions. A lot of CTF challenges will require you to be comfortable with Python scripting to automate some method of solving or brute-forcing the flag, so I recommend to continuosly try and improve your skillset. This can take the form of scripting something in python even if it's not really necessary. The more hands-on time you can put into it, the more comfortable and efficient you will become.

## Useful Functions
This section will walk you through various Python functions that should help you in CTF challenges and/or just speed up your python scripting process.

### `enumerate()`
This allows you to return each value from some iterable object with its index value, as a tuple. For example:
```python
>>> l = ['a','b','c']
>>> for x in enumerate(l):
...     print(x)
...     
... 
(0, 'a')
(1, 'b')
(2, 'c')
```
We can see that each item from the list is returned in a tuple with its index value. This can be used as a replacement for using the standard `for x in range(len(your_list))` to loop through each index of list. Let's compare:
```python
>>> l = ['a','b','c']
>>> for idx, val in enumerate(l):
...     print(f"{idx} - {val}")
...     
... 
0 - a
1 - b
2 - c
```
```python
>>> l = ['a','b','c']
>>> for idx in range(len(l)):
...     print(f"{idx} - {l[idx]}")
...     
... 
0 - a
1 - b
2 - c
```
As you can see, to get the value using the second method you have to pass the index into the list to get the value, when you didn't have to for the first method.

### f-string
You may have noticed above, I am using some strange looking print statement. This is called an f-string, as you lead the string " " with an *f*" ". This basically allows you to pass in variables right into the string using curly braces instead of having to concatenate strings and variables or using the `.format()` method. Let's compare:
```python
>>> fname = "daniel"
>>> lname = "getter"
>>> print(f"Hello, my name is {fname} {lname}")
Hello, my name is daniel getter
>>> print("Hello, my name is " + fname + " " + lname)
Hello, my name is daniel getter
>>> print("Hello, my name is {} {}".format(fname, lname))
Hello, my name is daniel getter 
```
The differences are not huge, but it can definitely help speed up the process of creating strings with variables.

### `list()`
`list()` is super simple. As the name implies, it just makes a list of any iterable object that you give it. I find it the most useful when you have some string and you want to make a list containing each letter seperately. For example:
```python
>>> phrase = "according to all known laws of aviation"
>>> lst = list(phrase)
>>> print(lst)
['a', 'c', 'c', 'o', 'r', 'd', 'i', 'n', 'g', ' ', 't', 'o', ' ', 'a', 'l', 'l', ' ', 'k', 'n', 'o', 'w'
, 'n', ' ', 'l', 'a', 'w', 's', ' ', 'o', 'f', ' ', 'a', 'v', 'i', 'a', 't', 'i', 'o', 'n']
```
Now that we have a list, we can use any list methods we want to interact with the data.

### `iter()` and `next()`
`iter()` is quite similar to `list()` but it makes an *iterator* instead of an *iterable* object. Yeah, there's a differnece, you can google it if you want. I generally use it only if I need to use `next()`, which returns the next item in an *iterator* (but not when used with an *iterable* object; so it won't work on lists, unless you convert that list to an iterator with `iter()` 🙃). For example:
```python
>>> vowels = ['a', 'e', 'i', 'o', 'u'] # this would work as just a string "aeiou" as well
>>> vowels_iter = iter(vowels)
>>> print(next(vowels_iter))
a
>>> print(next(vowels_iter))
e
>>> print(next(vowels_iter))
i
>>> print(next(vowels_iter))
o
>>> print(next(vowels_iter))
u
```
You might think to yourself that you could just use a loop to iterate over a list and do the same thing, and you would be right, in this case. However, there are valuable use cases for using `next()`. Let's look at some code I wrote as an example ([next.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20300/next.py)):
```python
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
```
```console
$ python3 next.py
~!@#@ $% ^& *() ~!(~ ( -@@ %!&=+_ -@ (-+@ ~& [+)
```
This script takes in a message and converts it to special characters to hide its true meaning. This is just a simple substitution cipher. So what's special about it? Well, we need to make sure that one letter is mapped to one special character. The first step is to iterate over every character in the message. Next we check if the letter is already mapped to a special character. If it is, we can continue to the next letter. If the letter is a space (" "), then we don't do anything. If neither of those are the case, then it means we have a letter than has yet to be mapped to a special character. This is where we use `next()` to select the next special character in our iterator containing 26 special characters. 

You may ask yourself what would happen if we used an index in our for loop instead of just values, and then use that index to select items from the special characters; something like this:
```python
for idx, letter in enumerate(message):
	if letter in mapping:
		continue
	elif letter == " ":
		continue
	else:
        # you'd have to make special_chars a list() instead of iter() 
        # to select items using an index
		mapping[letter] = special_chars[idx] 
```
Hopefully you see what the issue is here. Let's walk through each step of the for loop if we were to run it:
```console
Index: 0 - Special Char: '~'
Index: 1 - Special Char: '!'
Index: 2 - Special Char: '@'
Index: 3 - Special Char: '#'
Index: 4 - 'e' is already mapped
Index: 5 - It's a space
Index: 6 - Special Char: '^'
Index: 7 - Special Char: '&'
Index: 8 - It's a space
Index: 9 - Special Char: '('
Index: 10 - Special Char: ')'
Index: 11 - It's a space
Index: 12 - Special Char: '='
Index: 13 - Special Char: '+'
Index: 14 - Special Char: '_'
Index: 15 - It's a space
Index: 16 - 't' is already mapped
Index: 17 - 'h' is already mapped
Index: 18 - 'a' is already mapped
Index: 19 - 't' is already mapped
Index: 20 - It's a space
Index: 21 - 'a' is already mapped
Index: 22 - It's a space
Index: 23 - Special Char: '.'
Index: 24 - 'e' is already mapped
Index: 25 - 'e' is already mapped
Index: 26 - It's a space
Index: 27 - 's' is already mapped
Index: 28 - 'h' is already mapped
Index: 29 - 'o' is already mapped
Traceback (most recent call last):
  File "next.py", line 22, in <module>
    mapping[letter] = special_chars[idx]
IndexError: list index out of range
```
Any time in the for loop if a letter is already mapped or the letter is a space, we move on to the next iteration and increasing the index. This means that we end up skipping special characters at those indices. Index 4 and 5 contain $ and % which are then not used as you can see in the output. It's not the end of the world that we skip some special characters, but the main issue is that we end up with an `IndexError: list index out of range` cause after skipping enough special characters we run out of ones to use for new letter mappings.

I probably spent wayyy too much time explaining the use cases for `iter()` and `next()`, especially since I use them like 2% of the time. Whoops. At least you understand them well now, I hope.

### `.join()`
`join()` is a function that creates a string from an iterable object by joining each item with a given seperator. For example:
```python
>>> lst = ["a", "b", "c"]
>>> ".".join(lst)
'a.b.c'
>>> " ".join(lst)
'a b c'
>>> "".join(lst)
'abc'
```

### List Comprehension
List comprehension is a quick and easy way of creating a list from another list. Usually, if we want to create a list from another list, we would write a for loop with a conditional. Like so:
```python
>>> fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
>>> newlist = []
>>> 
>>> for x in fruits:
...   if "a" in x:
...     newlist.append(x)
... 
>>> print(newlist)
['apple', 'banana', 'mango']
```
List comprehension makes this super quick and easy, this is all you need:
```python
>>> fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
>>> 
>>> newlist = [x for x in fruits if "a" in x]
>>> 
>>> print(newlist)
['apple', 'banana', 'mango']
```
| output to append to list |       loop        |  conditional  |
| :----------------------: | :---------------: | :-----------: |
|           `x`            | `for x in fruits` | `if "a" in x` |

Or if you want an if/else:
```python
>>> newlist = [x if "a" in x else f"{x} is not a fruit" for x in fruits]
>>> newlist
['apple', 'banana', 'cherry is not a fruit', 'kiwi is not a fruit', 'mango']
```
| output if true |  conditional  |  else  |     output if false     |       loop        |
| :------------: | :-----------: | :----: | :---------------------: | :---------------: |
|      `x`       | `if "a" in x` | `else` | `f"{x} is not a fruit"` | `for x in fruits` |

We can use this type of list comprehension with `.join()` to immediately create a new string from items in a list. This can be directly applied in our `next.py` script. If you remember, we constructed a new string from our letter to special character mappings with:
```python
secret = ""
for letter in message:
	if letter == " ":
		secret += " "
	else:
		secret += mapping[letter]

print(secret)
----------------------------------------------------------
output: "~!@#@ $% ^& *() ~!(~ ( -@@ %!&=+_ -@ (-+@ ~& [+)"
```
This can be shortened to one list comprehension and `.join()` statement like so:
```python
crazy = "".join([" " if letter == " " else mapping[letter] for letter in message])
print(crazy)
----------------------------------------------------------
output: "~!@#@ $% ^& *() ~!(~ ( -@@ %!&=+_ -@ (-+@ ~& [+)"
```
Try putting it in `next.py` yourself and you should see that it works exactly the same!


### `ord()`, `chr()`, and `hex()`
These functions are helpful in turning a character into its integer representation and hex representation or vice-versa. If you go to http://www.asciitable.com/ you should see that each ASCII character has a decimal and hexadecimal representation. For example, "A" is 65 in decimal and 41 in hex. Being able to convert between these is very helpful in many situations, which you will probably encouter in other courses. Here's how it works:
```python
>>> ord("A")
65
>>> hex(65)
'0x41'
>>> chr(65)
'A'
```

### `map()`
`map()` takes an iterable object and applies a given function to each item. It returns a *map* object, but it can be converted to a list with `list()`. Let's say we want to perform a simple operation on every item in a list, such as shifting every letter of a sentence by 3 letter (a -> d, z -> c). Instead of looping through every letter in the sentence, shifting it, and appending it to a list, we can do all of that with `map()`, like so ([shift.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20300/shift.py)):
```python
letters = list("its wings are too small to get its fat little body off the ground")

def shift(letter, shift=3):
	if letter == " ":
		return " "
	else:
		return (chr((ord(letter) + shift - 97) % 26 + 97))

shifted_list = list(map(shift, letters))
shifted = "".join(shifted_list)
print(shifted)
----------------------------------------------------------
output: lwv zlqjv duh wrr vpdoo wr jhw lwv idw olwwoh ergb rii wkh jurxqg
```
The `shift()` function will take two parameters, a single letter and an amount to shift the letter by, which will default to 3 (I will explain why later). If the letter is a space, we return a space, if not, we perform a mathematical operation. If it seems confusing, here is how it looks step by step:
```
for letter "a":
	ord("a") = 97
	97 + 3 = 100 ("d")
	100 - 97 = 3
	3 % 26 = 3
	3 + 97 = 100
	chr(100) = "d"
-----------------------
for letter "":
	ord("z") = 122
	122 + 3 = 125 ("}")
	125 - 97 = 28
	28 % 26 = 2
	2 + 97 = 99
	chr(99) = "c"
```
We then use `map()` to run the `shift()` function for every letter in our sentence, turn that *map* object into a list, and then make a string out of the list with `join()`. Sweet!

We can improve this a bit by adding the ability to change the shift value outside of the function. Here is the code you would need to use instead:
```python
from itertools import repeat

letters = list("its wings are too small to get its fat little body off the ground")

def shift(letter, shift=3):
	if letter == " ":
		return " "
	else:
		return (chr((ord(letter) + shift - 97) % 26 + 97))

shifted_list = list(map(shift, letters, repeat(5)))
shifted = "".join(shifted_list)
print(shifted)
----------------------------------------------------------
output: nyx bnslx fwj ytt xrfqq yt ljy nyx kfy qnyyqj gtid tkk ymj lwtzsi
```
I will not explain why this works or what is happening in this course, but feel free to look how `map` works and why we need to use `itertools.repeat` to make this work.

### Lambda Functions
Lambda functions, or anonymous functions, allow you to run functions in one line without having to define it/give it a name. Here's an example:
```python
>>> double = lambda x: x * 2
>>> double(5)
10
```
`lambda` syntax is as follows: `lambda <arguments>: <expression>`. In our case, we only have one argument `x` and the expression `x * 2`. We assign this lambda function to `double`, so when we call it with the argument `5`, our result is `5 * 2 = 10`. Lambda functions are the most useful when used with `map()`. Let's look at an example, using our prevoius `shift.py` code:
```python
from itertools import repeat

letters = list("its wings are too small to get its fat little body off the ground")

shifted_list = list(map(lambda letter, shift: " " if letter == " " else (chr((ord(letter) + shift - 97) % 26 + 97)), letters, repeat(3)))

shifted = "".join(shifted_list)
print(shifted)
----------------------------------------------------------
output: lwv zlqjv duh wrr vpdoo wr jhw lwv idw olwwoh ergb rii wkh jurxqg
```
We can see we define the a lambda function inside of map where you would usually pass in the name of a fucntion, such as our `shift()` function from before. It might still be easier and definitely more readable to use a normal function in this case, but you should nonetheless know about it, as it may come in handy in your future. 

## Next Steps
 - find ways to improve [next.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20300/next.py)
 - write a script to take the output of [next.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20300/next.py) and turn it into letters
 - find ways to improve [shift.py](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/SCRIPT%20300/shift.py)

## More Resources
- https://www.programiz.com/python-programming/methods/built-in
- https://www.programiz.com/python-programming/list-comprehension
- https://www.programiz.com/python-programming/anonymous-function
- https://docs.python.org/3/library/itertools.html#itertools.repeat
- https://stackoverflow.com/a/27025330

## Creators

**Daniel Getter**

Enjoy :metal:
