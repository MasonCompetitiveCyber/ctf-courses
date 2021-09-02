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
Files and Directories each have assigned rights for the owner of the file, members of the group and related users as well as everybody else. Ownership of files can be broken down into 3 Parts

  USER
    A user is the owner of the file the person who created the file becomes the owner
    
  GROUP
    A user group can contain multiple users in it so that all users in a group can have access to said file with out having to have to manually assign accces to each individual
    
    All users
      Any other user who has access to the file they neither created or belongs to a group also know as world permissions
      
  how does linux determine between these three user types so that one user does not impact anothers file. This is where permissions come into play
  
  Permissions can be broken down into 3 parts
    
      READ (4)
        This gives you the ability to open and read a file. access with a directory gives you the ability to read its content 
        
      WRITE (2)
        refers to the ability a user's ability to write or modify a file or directory
        
       EXECUTE(1)
         affects the abiltiy of a user to execute a file or view the contents of a directory
         
    Viewing the permissions
        You can view the permissions with the ls -l 
        
 | '$ls -l testfile'|
-rwxrwxr--  1 amrood   users 1024  Nov 2 00:10  testfile

<p align="center">
    <img src="https://linuxcommand.org/images/file_permissions.png" width=75%  height=75%><br>
    <em>source: https://linuxconfig.org/filesystem-basics</em>
</p>


Advanced Permissions

The special permissions flag can be marked with any of the following:

    _ – no special permissions
    d – directory
    l– The file or directory is a symbolic link
    s – This indicated the setuid/setgid permissions. This is not set displayed in the special permission part of the permissions display, but is represented as a s in the read portion of the owner or group permissions.
    t – This indicates the sticky bit permissions. This is not set displayed in the special permission part of the permissions display, but is represented as a t in the executable portion of the all users permissions


The chmod command is used to change the permissions of a file or directory. To use it, we specify the desired permission settings and the file or files that we wish to modify. There are two ways to specify the permissions. In this lesson we will focus on one of these, called the octal notation method.

It is easy to think of the permission settings as a series of bits (which is how the computer thinks about them). Here's how it works:


       | number | Permission type        | symbol |
|--------|------------------------|--------|
| 0      | no permission          | -      |
| 1      | execute                | -x     |
| 2      | write                  | -w-    |
| 3      | execute+write          | -wx    |
| 4      | read                   | r-     |
| 5      | read + execute         | r-w    |
| 6      | read + write           | rw-    |
| 7      | read + write + execute | rwx    |

These are the numerical and character assigments for the respective permission types

Value 	Meaning
777 	(rwxrwxrwx) No restrictions on permissions. Anybody may do anything. Generally not a desirable setting.
755 	(rwxr-xr-x) The file's owner may read, write, and execute the file. All others may read and execute the file. This setting is common for programs that are used by all users.
700 	(rwx------) The file's owner may read, write, and execute the file. Nobody else has any rights. This setting is useful for programs that only the owner may use and must be kept private from others.
666 	(rw-rw-rw-) All users may read and write the file.
644 	(rw-r--r--) The owner may read and write a file, while all others may only read the file. A common setting for data files that everybody may read, but only the owner may change.
600 	(rw-------) The owner may read and write a file. All others have no rights. A common setting for data files that the owner wants to keep private. 

these are some example configurations


SPECIAL PERMISSIONS
Normally, on a unix-like operating system, the ownership of files and directories is based on the default uid (user-id) and gid (group-id) of the user who created them. The same thing happens when a process is launched: it runs with the effective user-id and group-id of the user who started it, and with the corresponding privileges. This behavior can be modified by using special permissions.


The setuid bit

When the setuid bit is used, the behavior described above it's modified so that when an executable is launched, it does not run with the privileges of the user who launched it, but with that of the file owner instead. So, for example, if an executable has the setuid bit set on it, and it's owned by root, when launched by a normal user, it will run with root privileges. It should be clear why this represents a potential security risk, if not used correctly.

ls -l /bin/passwd
-rwsr-xr-x. 1 root root 27768 Feb 11  2017 /bin/passwd

How to identify the setuid bit? As you surely have noticed looking at the output of the command above, the setuid bit is represented by an s in place of the x of the executable bit. The s implies that the executable bit is set, otherwise you would see a capital S. This happens when the setuid or setgid bits are set, but the executable bit is not, showing the user an inconsistency: the setuid and setgit bits have no effect if the executable bit is not set. The setuid bit has no effect on directories.

The setgid bit

Unlike the setuid bit, the setgid bit has effect on both files and directories. In the first case, the file which has the setgid bit set, when executed, instead of running with the privileges of the group of the user who started it, runs with those of the group which owns the file: in other words, the group ID of the process will be the same of that of the file.

When used on a directory, instead, the setgid bit alters the standard behavior so that the group of the files created inside said directory, will not be that of the user who created them, but that of the parent directory itself. This is often used to ease the sharing of files (files will be modifiable by all the users that are part of said group). Just like the setuid, the setgid bit can easily be spotted (in this case on a test directory):

ls -ld test
drwxrwsr-x. 2 egdoc egdoc 4096 Nov  1 17:25 test

This time the s is present in place of the executable bit on the group sector.
The sticky bit

The sticky bit works in a different way: while it has no effect on files, when used on a directory, all the files in said directory will be modifiable only by their owners. A typical case in which it is used, involves the /tmp directory. Typically this directory is writable by all users on the system, so to make impossible for one user to delete the files of another one, the sticky bit is set:

$ ls -ld /tmp
drwxrwxrwt. 14 root root 300 Nov  1 16:48 /tmp

In this case the owner, the group, and all other users, have full permissions on the directory (read, write and execute). The sticky bit is identifiable by a t which is reported where normally the executable x bit is shown, in the "other" section. Again, a lowercase t implies that the executable bit is also present, otherwise you would see a capital T.
How to set special bits

Just like normal permissions, the special bits can be assigned with the chmod command, using the numeric or the ugo/rwx format. In the former case the setuid, setgid, and sticky bits are represented respectively by a value of 4, 2 and 1. So for example if we want to set the setgid bit on a directory we would execute:

$ chmod 2775 test

With this command we set the setgid bit on the directory, (identified by the first of the four numbers), and gave full privileges on it to it's owner and to the user that are members of the group the directory belongs to, plus read and execute permission for all the other users (remember the execute bit on a directory means that a user is able to cd into it or use ls to list its content).

The other way we can set the special permissions bits is to use the ugo/rwx syntax:

$ chmod g+s test

To apply the setuid bit to a file, we would have run:

$ chmod u+s file

While to apply the sticky bit:

$ chmod o+t test

The use of special permissions can be very useful in some situations, but if not used correctly the can introduce serious vulnerabilities, so think twice before using them.



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
