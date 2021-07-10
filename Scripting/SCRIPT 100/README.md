<h1 align="center">SCRIPT 100</h1>
  <p align="center">
     Bash Scripting
  </p>

### Table of contents

- [Prerequisites](#prerequisites)
- [Introduction](#introduction)
- [Basics](#basics)
- [Creating Our First Bash Script: Network Ping Scan](#creating-our-first-bash-script-network-ping-scan)
    - [If/Else](#ifelse)
    - [Variables](#variables)
    - [For Loops](#for-loops)
    - [Bringing It All Together](#bringing-it-all-together)
- [Use Cases](#use-cases)
- [Next Steps](#next-steps)
- [More Resources](#more-resources)
- [Creators](#creators)

## Prerequisites
- Linux 100, 200, 300
    - You should be comfortable with the linux CLI and with linux commands

## Introduction
In this course you will learn the basics of local scripting in bash and python. *Local* just means that we are not interacting with remote endpoints, which will be discussed in the next course, SCRIPT 200. Knowing scripting is extremely useful as it will allow you to quickly solve problems and automate solutions using code. Know, you might be wondering what scripting even means, and how is it different than programming? Well, here is a widely accepted distinction: *"all scripting languages are programming languages, but the theoretical difference between the two is that scripting languages do not require the compilation step and are rather interpreted. For example, normally, a C program needs to be compiled before running whereas normally, a scripting language like JavaScript, PHP, or Python need not be compiled."* (https://www.geeksforgeeks.org/whats-the-difference-between-scripting-and-programming-languages/). If you don't know what a compiled or interpreted language is, you can read some more about them [here](https://www.geeksforgeeks.org/difference-between-compiled-and-interpreted-language/) and [here](https://www.freecodecamp.org/news/compiled-versus-interpreted-languages/). 

Now that I've told you the general description, we will kind of disregard that definition for our purposes. In my eyes, scripting is using a programming language to quickly solve a problem or automate a task. If, for some reason, I decide it is easier to write a short program in C to solve a problem or challenge, I still think it's considered scripting even though C is a compiled language. But that's just my opinion, I don't really care for the semantics. 

## Basics
One very useful skill to have when working in linux is bash scripting. Even super simple bash scripts can make your life much easier. A bash script is really just a collection of bash commands written out in a plain text file, conventionally given a `.sh` extensino. These commands are anything you can run normally in the command line, such as `ls`, `cp`, etc. 

I'll start with a practical example. In my kali vm, I often find myself needing to fix a weird resolution bug to set it back to 1920x1080. I had found a solution online that required running 3 bash commands which worked well for me. Instead of writing those commands down somewhere and re-typing them out every time I had to fix the resolution bug, I could just put them in a bash script. Let's take a look:

```bash
#!/bin/bash
xrandr --newmode "1920x1080"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
xrandr --addmode Virtual1 1920x1080
xrandr --output Virtual1 --mode 1920x1080
```

Let's break this down. First, we see the top line contains `#!/bin/bash`. The `#!` is called a shebang, which tells the linux OS what interpreter to use to parse the rest of the file. In this case, we are telling it to use bash. The following three lines of the script are all just separate bash commands. When bash runs this script, it will just execute each one in order. Simple enough. But how do you run it?

The first step to running a bash script is to set its file permissions to allow file execution. This can be done with a `chmod +x your_file.sh`. Next, you need to run the bash script like so: `./your_file.sh`. The `./` just denotes the file path of your bash script, which is the one you're in after you just made the bash script. If you're in another directory, you'd have to replace `./` with the file path to your bash script. 

## Creating Our First Bash Script: Network Ping Scan
I find the best way to learn new things is to do something hands-on, so let's create our first simple bash script. The goal of this script is to take in some user input for a network address, and given that, send a ping to all possible hosts on that network to see if they are up. 

### If/Else
The first thing we'll want to do is check if the user actually supplied any input. This means we have to start with an If/Else statement. The general format of an if/else statement in bash is:
```bash
if [[ some condition ]]
then
    <commands to run if condition evaluates to true>
else
    <commands to run if condition evaluates to false>
fi
```
*p.s. there is a differnece between using [ ] and [[ ]] for the conditional statement which I barely know and won't go into here, so you can google it if you want.*

### Variables
Now that we know the general structure of an if/else, we have to create the conditional statement to check if the user provided some command line argument as input. Bash stores command line arguments in variables denoted by `$1` for the first argument, `$2` for the second, and so on. If the user only needs to supply one argument, we should just check if `$1` is anything but empty. If it's empty, we should tell the user that they need to supply a network address and quit the program. Let's try putting some of this together.

```bash
#!/bin/bash

if [[ $1 == "" ]]
then
    echo "Please provide a network address to scan (ex: ./pingscan.sh 192.168.18)"
else
    echo "Placeholder for running the rest of our program"
fi
```

Make the script executable and now we can test it.

```console
$ ./pingscan.sh  
Please provide a network address to scan (ex: ./pingscan.sh 192.168.18)
```
```console
$ ./pingscan.sh 192.168.1  
Placeholder for running the rest of our program
```

Perfect!

### For Loops
Our next task will require using a loop to iterate over all numbers between 1 and 254. To do this, we can use a for loop. Basic for loop syntax looks like this:

```bash
for <item> in <list>
do
    <commands to run>
done
```

We want our `<list>` to be numbers from 1 to 254. This can be done in a couple ways. One way is to use the bash command `seq`. We can pass in two arguments, the firt number of a sequence and the last. For example:
```console
$ seq 1 254
1
2
.
.
.
253
254
```
Okay, so if we want to use this command to generate our sequence of numbers from 1 to 254, how do we do that? We need to basically capture the output of that command within bash and use it as a variable. This is done fairly simply. All we have to do is encase the command in `$()`, so it will become `$(seq 1 254)`. This is useful if we want to set that value to a variable, such as `numList=$(seq 1 254)`, but we can skip that and use it directly in our for loop statement, like this:
```bash
for ip in $(seq 1 254)
do
    <commands to run>
done
```
In the above code, the for loop will iterate over every number in the sequence and assign it to a variable `ip`. We can then reference that variable inside of the `do` section of the for loop. Now we have enough knowledge to finish the script.

### Bringing It All Together
Here is the final script:
```bash
#!/bin/bash

if [[ $1 == "" ]]
then
    echo "Please provide a network address to scan (ex: ./pingscan.sh 192.168.10)"
else
    for ip in $(seq 1 254)
    do
            ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &
    done
fi
```

The only thing that should look new to you is the long ping command in the for loop. Let's break it down (hopefully you should know this from the Linux courses, but I'll provide it here just in case). 

`ping -c 1 $1.$ip`
- `-c 1` is just telling ping to send one ping instead of the default infinite
- `$1.$ip` is concatenating our two variables `$1` (user-provided argument holding the network address) a "." and `$ip` (number 1-254). This will create a full ip address, such as `192.168.18.1`, `192.168.18.2`, etc. 

`grep "64 bytes"`
- If a ping is successful, you will generally see output that looks like `64 bytes from 192.168.18.128: icmp_seq=1 ttl=64 time=0.019 ms`. If not, it won't show that line. The grep command is basically checking if that line exists

`cut -d " " -f 4`
- This command is using the `cut` bash command to take the 4th (`-f 4`) field after splitting a given string using space as a delimeter (`-d " "`)
- If you look at the sample successful ping output I provided above, you'll the that the 4th item if delimeting by spaces is the target IP address of the ping

`tr -d ":"`
- After the `cut` command, we would have a value such as `192.168.18.128:`, but we don't want that trailing ":", so we use `tr` and specify the ":" with `-d` to get rid of it

`&`
- this symbol tells bash to run a command in the background which allows for other commands to be run and not wait for the current one to finish
- this means we aren't waiting for each ping to finish before moving on to the next, making this a much faster process

Let's run it!
```console
$ ./pingscan.sh 192.168.18
192.168.18.2
192.168.18.128
```

This output tells me that there are two hosts accepting ping requests, 192.168.18.2 and 192.168.18.128. This makes sense for me because 192.168.18.128 is my localhost address and 192.168.18.2 is the gateway. Awesome!

## Use Cases
I find bash scripting the most useful when I find the easiest solution is through a variety of linux/bash commands. As we saw with the long command used in the ping scanner (`ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &`), these commands can be very powerful when used together. We will see in the next course that Python is super great to use in most situations when scripting, but bash scripts tend to be the better option when needing to utilize the power of linux commands. For example, if I'm dealing with some command output and only want a specific column, it's super easy to use `cut` or `awk` to pull it out, so I find myself using bash scripting to quickly filter the data I'm working with and then do the rest in python.

## Next Steps
This was quite a short course, but understanding just the basics of bash scripting can cover most of the cases you might use it for. If you are interested in teaching yourself more and getting more comfortable with it, it would definitely be beneficial (I keep telling myself I will, but never do). One great way to try and expand your skills and comfort is to take the ping scanner we just made and improve it. At its current state, it is quite rudementary. Here's what you can do:

- allow the user to input a network address with a specific subnet or range of addresses
- use another method for getting a sequence of numbers, such as `{1..254}`
- use a while loop instead of a for loop
- add descriptive text to the output
- use a function to run the ping command and call that function within a loop
- output the results to a file instead of stdout
- set a variable to "64 bytes" and use the variable with grep instead of the string
- whatever else your heart desires

## More Resources
- https://ryanstutorials.net/bash-scripting-tutorial/
- https://devhints.io/bash

## Creators

**Daniel Getter**

Enjoy :metal:
