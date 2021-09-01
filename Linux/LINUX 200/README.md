<h1 align="center">LINUX 200 (Work in Progress)</h1>
  <p align="center">
     Linux Basics 
  </p>

### Table of contents

- [Introduction](#introduction)
- [Filesystem](#filesystem)
  - [Filepaths](#filepaths)
  - [Executable File Path](#executable-file-path)
- [CLI](#cli)
  - [Shortcuts](#shortcuts)
- [File Permissions](#file-permissions)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)


## Introduction
This course will walk you through the basics of working in Linux. It will cover the filesystem structure, basic command-line interface (CLI) commands, and file interaction.

## Filesystem
The first thing you should have general understanding of when using Linux is the filesystem heirarchy. If you're a Windows user, you're probably comfortable with how the filesystem is layed out such as having Documents, Downloads and so forth in your user folder. There are also other directories like "Program Files" and "Windows" that live in your C:\ directory which hold other types of files. This is the same premise in Linux.

The image below gives a pretty good overview of the filesystem heirarchy and the main functions of each directory.

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/linux/filesystem.png" width=75%  height=75%><br>
    <em>source: https://linuxconfig.org/filesystem-basics</em>
</p>

Let's break these down a bit. You won't need to know all of these, so I will only discuss those that you'd end up interacting with more regularly.

First off, `/`, the root directory. By "root" directory, this really means that all of the other directories are located here. 

Next, we have `/bin`. This holds "binaries," which is just a term for executable files. In this case, it holds the majority of commands that users are able to run in linux. Linux commands are really just pieces of executable code, so when you type a command, it is just running a piece of executable code to do something. I will discuss how Linux knows where to find the code for when you type a command in the [Executable File Path](#executable-file-path) section.

Another important directory is `/etc`. This holds all of the configuration files for the operating system and various other programs. A couple examples is the `/etc/shadow` and `/etc/passwd` files which hold information about the users on the system. 

One of the most common directories you'll be using is `/home`. This is where you'll find all the user-specific directories. For example, in Kali Linux you should be logged in as the "kali" user, who's home folder is located in `/home/kali`. Any other users on the system will also have folders in `/home`.

`/opt` isn't the most important, but this is where you should put any software or tools you download from third-party sources.

`/tmp` is self-explanatory. It holds temporary files which get wiped after reboot.

`/root` is just the home folder for the "root" user, just like you have one for "kali".

The other directories are important to know, but not necessary, so I won't go into more detail about them here.

### Filepaths
You might wonder why there's a `/` in front of the various directory name and that's because it is a filepath. To get to the `home` directory, for example, you first have to get into the root directory, or `/`. Then to get into your "kali" user directory, you'd get the filepath `/home/kali`, and so on. It may be abit confusing because slashes, `"/"` are also used to delineate the folders, such as between "home" and "kali". The important distinction is that if the filepath starts with a `"/"`, then that slash is referencing the root directory and is called an absolute file path. On the other hand, there are relative file paths. Instead of starting at the root directory (`"/"`), you can start at the current directory you're located in. This is denoted by a period `"."`. Let's say we're in the `/home` directory and want to reference the "kali" folder. We can use the relative file path `./kali`. The period says to start in the current directory and then go into "kali". If you want to reference the directory above the current one (also known as the parent directory), then you can use two periods, `".."`. If you are in `/home/kali` and want to reference `/home/`, then you can use `../home`. 

### Executable File Path
Earlier I referenced the question about how Linux knows where an executable program is located whenever you type in a command. To do this, there is an "environment variable" called the `PATH`. This variable tells Linux which directories to look in when a user types in a command to find an executable program of the same name. For example, if you type in `"hello"` into the command line, then Linux will look in all the directories listed in the `PATH` variable for an executable file called "hello". Since this file doesn't exist, you would get a warning saying `"command not found"`. If it does exist, then that command runs. Some default directories listed in the `PATH` variable are `/bin`, `/usr/local/bin`, and `/usr/bin`. Since most system-wide commands have their respective binaries located in `/bin`, they would be found when a user types in that command and it will run.

## CLI
Now that you have a general sense how Linux operates, we can start getting familiar with the command-line interface, a.k.a the CLI. Here are some basic commands (these do not include all the available options, you can research those on your own using `man [command]` or `[command] --help` or google). I highly recommend playing around with these commands in your terminal to get used to how it all works.
| command  | what it do  |
|---|---|
| `cd [path]`  | change directory to path specified by `[path]` (can be absolute or relative)  |
| `ls`  | list files and directories in current directory  |
| `pwd`  | print out current directory path  | 
| `mv [path of file to move] [destination path]` | move a file from one directory to another (can also be used to rename files) |
|`cp [path of file to copy] [destination path]` | copy a file to another location |
| `cat [file path]` | print out the contents of a file|
| `less [file path]` | print ot contents of a file but only one screen at a time | 
| `man [command]`| read manual page for a command |
| `head [file path]` and `tail [file path]` | print out the first x number of lines of a file or the last x number of lines of a file respectively
| `mkdir [path/name of directory]`| create a directory |
| `rm [file/directory path]`| delete a file or directory (deleting a directory will need extra options set)|
| `unzip [file path]`| unzip a .zip file |
| `touch [file path]` | create an empty file |
| `vim [file path]` or `nano [file path]`| open a terminal file editor on a file |

Now, this is obviously not an exhaustive list because that would take up an infeasible amount of space. However, knowing these will help you get oriented and used to the Linux CLI. 

### Shortcuts
To be completed

## File Permissions
To be completed

## Practice
- https://tryhackme.com/room/linuxfundamentalspart1
- https://tryhackme.com/room/linuxfundamentalspart2
- https://tryhackme.com/room/linuxfundamentalspart3

## More Resources
- https://tldp.org/LDP/Linux-Filesystem-Hierarchy/html/index.html
- https://linuxconfig.org/filesystem-basics
- https://www.digitalocean.com/community/tutorials/an-introduction-to-linux-basics
- https://www.hostinger.com/tutorials/linux-commands

## Creators

**Daniel Getter**

Enjoy :metal: