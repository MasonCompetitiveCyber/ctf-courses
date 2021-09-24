<h1 align="center">LINUX 300</h1>
  <p align="center">
     Useful Commands
  </p>

### Table of contents

- [Introduction](#introduction)
- [Commands](#commands)
  - [`awk`](#awk)
  - [`cut`](#cut)
  - [`tr`](#tr)
  - [`uniq`](#uniq)
  - [`sort`](#sort)
  - [`wc`](#wc)
  - [`grep`](#grep)
  - [`find` and `locate`](#find-and-locate)
  - [`wget` and `curl`](#wget-and-curl)
- [Pipe Operator](#pipe-operator)
- [Man Pages and `--help`](#man-pages-and---help)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction
This course will walk you through Linux commands and tools that are very useful in CTFs. There are a lot more, but those generally fall under different categories like crypto, steg, and so on, so you will find those in their respective courses.

## Commands
In no particular order, here are various useful commands:

### `awk`
`awk` is a command that is very useful when wanting manipulate some data. It is very powerful and has many uses, but I will show the case which I use it for the most. If you want to read more about it, there will be a link in the [More Resources](#more-resources) section.

Let's say we are given some log data that looks like this:
```
Jun 15 12:12:34 combo sshd(pam_unix)[23397]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23397]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23395]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23395]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23404]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23404]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23399]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23399]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23406]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23406]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23396]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23394]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23407]: check pass; user unknown
Jun 15 12:12:34 combo sshd(pam_unix)[23394]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
```
For whatever reason, a CTF challenge for example, we need to extract the timestamp of every log entry. We can do this quite simply with `awk`. Here is the solution, and then I will explain it:
```console
# awk '{print $3}' log.txt
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
```
By default, `awk` splits output based on spaces. Inside the single quotes, we tell `awk` to print the 3rd (`$3`) column ov every row from `awk-example.txt`. *Note: awk counts starting from 1, not 0.* This was a quick and easy way to extract a subset of data that we could use for some other purpose.

`awk` has another pretty powerful feature to help in this data trimming, and that is the `-F` option. Let's say we wanted to get the last "column" of information (i.e. "authentication failure ..." or "check pass ..."). If we try to use just `awk`, it will split every word into a new column, so it won't be easy. Luckily, `awk`'s `-F` option allows us to specify the delimeter we want to use for splitting columns. In this case, let's split by the delimeter "`: `". 
```console
# awk -F ": " '{print $2}' log.txt
check pass; user unknown
authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
check pass; user unknown
authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
check pass; user unknown
authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
check pass; user unknown
authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
check pass; user unknown
authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
check pass; user unknown
check pass; user unknown
check pass; user unknown
authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
```
Notice that I didn't use just "`:`" as the delimeter, as there are colons in the timestamp, which would make it worse of a delimeter. The `": "` combination only happens once, right before the data we want, so we can specify the 2nd column and get the data we want. Yay!

### `cut`
`cut` is another useful tool when dealing with trimming down data. Let's look at the following example:
```console
# cut -d " " -f 3 log.txt
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
12:12:34
```
You should notice that this achieved the same thing as `awk '{print $3}' log.txt`. For the `cut` command, the `-d` option lets us specify the delimeter we want to use and the `-f` option is for the field number. 

I usually use cut for something else, and that is selecting some range of data. For example:
```console
# cut -c 17-44 log.txt
combo sshd(pam_unix)[23397]:
combo sshd(pam_unix)[23397]:
combo sshd(pam_unix)[23395]:
combo sshd(pam_unix)[23395]:
combo sshd(pam_unix)[23404]:
combo sshd(pam_unix)[23404]:
combo sshd(pam_unix)[23399]:
combo sshd(pam_unix)[23399]:
combo sshd(pam_unix)[23406]:
combo sshd(pam_unix)[23406]:
combo sshd(pam_unix)[23396]:
combo sshd(pam_unix)[23394]:
combo sshd(pam_unix)[23407]:
combo sshd(pam_unix)[23394]:
```
`cut` has the `-c` option that allows us to select the range of characters we want to select for our output. In this case, we selected the 17-44 characters. We can also use `nd-` or `-n` to say we want everything after or everything before a certain character index.

### `tr`
`tr` can perform operations like removing repeated characters, converting uppercase to lowercase, and basic character replacing and removing. I mainly use it to remove characters. For example, if I wanted to remove the colons from the list of times I got using `cut` in a previous example, I can do this:
```console
# cut -d " " -f 3 log.txt | tr -d ":"
121234
121234
121234
121234
121234
121234
121234
121234
121234
121234
121234
121234
121234
121234
```
If you haven't seen the `|` character before, it's called the "pipe" operator, which I will discuss in the later section [pipe operator](#pipe-operator). Anyways, we can see in the `tr` command I used, I used the `-d` option to specify which character I wanted to delete. Thus, we can see that the timestamp no longer has colons separating the hours, minutes, and seconds. This may be useful, for example in this case, if working with times that you want to sort as numbers and the colons might be getting in the way.

### `uniq`
The `uniq` operator can report or filter out repeating lines in a file. I added a duplicate line to our log.txt file so we can see this work. Let's say I wanted to count the number of occurences of a line in a file:
```console
# uniq -c log.txt
1 Jun 15 12:12:34 combo sshd(pam_unix)[23397]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23397]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23395]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23395]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23404]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23404]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23399]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23399]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23406]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23406]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23396]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23394]: check pass; user unknown
2 Jun 15 12:12:34 combo sshd(pam_unix)[23407]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23394]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
```
You can see the 2nd to last line has a "2" in front of it, as the `-c` option will count occurences of each line in a file.  If you `cat` the file normally, you will see that that line is duplicated. To print out duplicate lines only, use the `-d` option and to print out all non-duplicate lines, don't use any option.

### `sort`
`sort` does what you expect it to do, sort things. Taking the output of the previous command, let's sort by number of duplicates:
```console
# uniq -c log.txt | sort -n
1 Jun 15 12:12:34 combo sshd(pam_unix)[23394]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23394]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23395]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23395]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23396]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23397]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23397]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23399]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23399]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23404]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23404]: check pass; user unknown
1 Jun 15 12:12:34 combo sshd(pam_unix)[23406]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
1 Jun 15 12:12:34 combo sshd(pam_unix)[23406]: check pass; user unknown
2 Jun 15 12:12:34 combo sshd(pam_unix)[23407]: check pass; user unknown
```
We can see that the "2" is now at the bottom of the list. We used the `-n` option to sort numerically, as it will default to sorting by ASCII letters. You can read more by following the link about the `sort` function in the [More Resources](#more-resources) section.

### `wc`
`wc` stands for "word count" and thus becomes *almost* self-explanatory. It is mainly used for counting the words, lines, or bytes present in a file. Let's say we are interested in the number of lines in log.txt:
```console
# wc -l log.txt 
15 log.txt
```
The `-l` option allows us to tell `wc` to count the number of lines in a file. `-c` is for bytes and `-w` is for words. Again, more info is in the [More Resources](#more-resources) section.

### `grep`
`grep` is an exceptionally useful tool that you will probably use a lot. It is mostly used for finding a pattern of characters in a file; think of it as a search function (but it can generally be much more powerful if you know how to use it). For the most basic use-case, let's search our log.txt file for the word "failure":
```console
# grep "failure" log.txt
Jun 15 12:12:34 combo sshd(pam_unix)[23397]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23395]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23404]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23399]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23406]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
Jun 15 12:12:34 combo sshd(pam_unix)[23394]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
```
We got back all the lines that contain the word "failure", perfect. There are other options available that help you refine your search if needed, and you'll find the link, as always, in the [More Resources](#more-resources) section.

### `find` and `locate`
`locate` and `find` help you find files in your filesystem. `find` is a command to help you find files in your file heirarchy. For example, if I wanted to find a file with a name starting with "log" in my current directory:
```console
# find . -name log* 
./log.txt
```
It found our log.txt file! The `"."` just specified to look in my current directory. If you haven't seen `"*"` before, this is just a "wildcard" operator, which just means it can match anything. So if I had the following files in my directory: log.py, logarithm.txt, logging.c -- then they would also all match as they all start with "log" and end with whatever, thanks to the `*`. 

`locate` is arguably a better and faster version of `find`, as it uses a database to search instead of going manually though every directory. To update this database, run the command `updatedb`. Anyways, let's look through all files on my filesystem for any file named "log.txt":
```console
# locate log.txt
/opt/sublime_text/changelog.txt
/root/.Bytecode-Viewer/krakatau_12/Krakatau-master/Documentation/changelog.txt
/root/.ZAP/jbrofuzz/log/08.03.2021-log.txt
/root/.ZAP/jbrofuzz/log/10.05.2021-log.txt
/root/.ZAP/jbrofuzz/log/10.07.2021-log.txt
/root/.ZAP/jbrofuzz/log/14.05.2021-log.txt
/root/.ZAP/jbrofuzz/log/18.05.2021-log.txt
/root/.ZAP/jbrofuzz/log/19.06.2021-log.txt
/root/.ZAP/jbrofuzz/log/20.05.2021-log.txt
/root/.ZAP/jbrofuzz/log/26.05.2021-log.txt
/root/.ZAP/jbrofuzz/log/27.05.2021-log.txt
/root/Documents/CTFs/USCO/lvl1/Samsung/backup/sdcard/Android/data/com.microsoft.skydrive/cache/current_log.txt
/root/Documents/CTFs/USCO/lvl2/forensics/backup/sdcard/Android/data/com.microsoft.skydrive/cache/current_log.txt
/root/Documents/masoncc/linux/log.txt
/usr/lib/python3/dist-packages/mercurial/helptext/internals/linelog.txt
/usr/share/doc/util-linux/getopt_changelog.txt
/usr/share/seclists/Discovery/Web-Content/SVNDigger/context/log.txt
```
It went pretty fast for me and found every instance of "log.txt" in my filesystem. There are many options available for this command, so check them out at the link in the [More Resources](#more-resources) section.

### `wget` and `curl`
`wget` and `curl` are two commands that help downloading files from the internet. There are important differences between the two, but I will only show two examples of how to download things from the internet with them:
```console
# wget https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf
--2021-09-23 20:18:12--  https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf
Resolving file-examples-com.github.io (file-examples-com.github.io)... 185.199.111.153, 185.199.109.153, 185.199.108.153, ...
Connecting to file-examples-com.github.io (file-examples-com.github.io)|185.199.111.153|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 142786 (139K) [application/pdf]
Saving to: ‘file-sample_150kB.pdf’

file-sample_150kB.pdf                                100%[=====================================================================================================================>] 139.44K  --.-KB/s    in 0.01s   

2021-09-23 20:18:12 (11.8 MB/s) - ‘file-sample_150kB.pdf’ saved [142786/142786]
```
```console
# curl https://file-examples-com.github.io/uploads/2017/10/file-sample_150kB.pdf -o curl-example.pdf
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  139k  100  139k    0     0  3031k      0 --:--:-- --:--:-- --:--:-- 3098k
```

## Pipe Operator
As mentioned before, here is the section about the pipe operator `|`. This operator is meant to chain together the output from one command to the input of another as we saw in a couple prior examples. It let us take the output from the `cut` comamnd and use it as input to the `tr` command. We can chain as many commands as we want together, like so:
```console
# cat log.txt | awk '{print $5}' | cut -c 15- | tr -d "[]:" | sort | uniq -c 
2 23394
2 23395
1 23396
2 23397
2 23399
2 23404
2 23406
2 23407
```

## Man Pages and `--help`
If you ever need help figuring out how to use a command, you have three options. Man pages, `--help`, and Google. Man pages are the official documentation of the command which you can access using the command `man <command>`. Most commands also have a `--help` (sometimes also a `-h`) option for shorter and quicker access to help. 

## More Resources
- https://www.geeksforgeeks.org/awk-command-unixlinux-examples/
- https://www.geeksforgeeks.org/cut-command-linux-examples/
- https://www.geeksforgeeks.org/tr-command-in-unix-linux-with-examples/
- https://www.geeksforgeeks.org/uniq-command-in-linux-with-examples/
- https://www.geeksforgeeks.org/sort-command-linuxunix-examples/
- https://www.geeksforgeeks.org/wc-command-linux-examples/
- https://www.geeksforgeeks.org/grep-command-in-unixlinux/
- https://www.geeksforgeeks.org/find-command-in-linux-with-examples/
- https://www.geeksforgeeks.org/locate-command-in-linux-with-examples/
- https://www.geeksforgeeks.org/wget-command-in-linux-unix/
- https://www.geeksforgeeks.org/curl-command-in-linux-with-examples/
- https://daniel.haxx.se/docs/curl-vs-wget.html
- https://www.geeksforgeeks.org/piping-in-unix-or-linux/


## Creators

**Daniel Getter**

Enjoy :metal: