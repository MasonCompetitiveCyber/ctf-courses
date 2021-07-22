<h1 align="center">SCRIPT 320</h1>
  <p align="center">
     Python: File Manipulation
  </p>

### Table of contents

- [Prerequisites](#prerequisites)
- [Introduction](#introduction)
- [Opening a file](#Opening-a-file)
- [Reading](#Reading)
- [Writing](#Writing)
- [The problem](#The-problem)
- [More Resources](#more-resources)
- [Creators](#creators)

## Prerequisites
- Scripting 200
  - You should be comfortable with basic python programming (if/else, loops, functions)
- Scripting 300
  - You should be comfortable with using some more advanced python functions

## Introduction
This will introduce you to file manipulation and very basic OSINT research.

## Opening a file
Opening a file in python requires the use of the open() function. This function takes two parameters; filename/path, and [mode](https://www.w3schools.com/python/python_file_handling.asp). The most common use is to assign this function to a variable.
```python
f = open("path to file (/home/user/text.txt)", "w")
```
When opening files with this method you need to remember to close them by calling .close() on the variable when done.
```python
f.close()
```
Usually, the better way to open a file is through using the "with open" method. This will open the file as long as the code is being run within the indented block.
```python
with open("path to file", "w") as f:
    print("this code would run with the file open")

print("this code would run with the file closed")
```
Note: On linux you can use the normal "/" in the file path, however for windows you need to escape the "\\" with a second back slash like so "\\\".

The basic modes you'll need are x, a, and w.
- `"x"` - Create - will create a file, returns an error if the file exist.
- `"a"` - Append - will create a file if the specified file does not exist.
- `"w"` - Write - will create a file if the specified file does not exist.

You can also change to reading a file as (t)ext or as (b)inary by adding a `"t"` or `"b"` after the mode like so `"wt"`.

## Reading
There are two functions to read from a file.
- `read()` reads the whole text, or a specific amount of characters.
```python
with open("path to file", "r") as f:
    # The whole file
    content = f.read()
    # 3 characters
    content = f.read(3)
```
- `readline()` reads a single line and movies the courser to the next line.
```python
with open("path to file", "r") as f:
    # the first line
    content1 = f.readline()
    # the second line
    content2 = f.readline()
    # you can also loop through the lines like so
    for x in f:
        print(x)
```
- `readlines()` reads all the lines and turns them into a list, with each line being a new item.
```python
with open("path to file", "r") as f:
    content = f.readlines()
```
## Writing
There is only one function to write to a file in python, `write()`. Write will act differently depending on the mode you select.
- `"a"` - Append - Writes to the end of a file.
- `"w"` - Write - Erases content in the file and writes over it.
```python
with open("path to file", "w") as f:
    content = f.write("This will be the only thing in the file")
```
```python
with open("path to file", "a") as f:
    content = f.write("This will add this text to the file above!")
```
Additionally, python's string operators will work when writing to the file
- `"\n"`  -  New line - Makes a new line
- `"\t"`  -  Tab - Makes a tab


## The problem
You need the password to your friends laptop. The two hints he gave you is that he REALLY loves the bee movie script and math. For some odd reason he gave you a text file called "beeMovieScript.txt". You also know that your friend was recently learning about the bee reproductive cycle in his natural sciences class. Good luck!

## More Resources
- https://www.w3schools.com/python/python_file_handling.asp
- https://www.w3schools.com/python/python_file_open.asp

## Creators
**Michael Mazzatenta**