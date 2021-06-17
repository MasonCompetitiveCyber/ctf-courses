<h1 align="center">STEG 200</h1>
  <p align="center">
     More Image Steg
  </p>

### Table of contents

- [Introduction](#introduction)
- [Image LUT](#image-lut)
- [Bit Planes](#image-bit-planes)
- [XOR](#image-xor)
- [Files Within Files](#files-within-files)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

# Introduction
In this course, we will continue talking about methods of image steganography, including methods such as LUT manipulation, bit planes, XOR, and embedded files. There are almost an infinite amount of ways to hide information, so it's not feasible to go through all of them, but at least these should cover basic CTF steg problems.

# Image LUT
LUT stands for Lookup Table, which produce color images by mapping numbers to colors. LUT's are used for creating N-bit color images and color correcting. Unlike RGB color images that use bytes to code for RGB values for color, images like 8-bit color images will use an LUT. Here's an image to show how it works:

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/how-lut-works.png" width=60%  height=60%><br>
    <em>source: http://40two.info/barge/image_processing/Intro/PDF/Lookup_Tables.pdf</em>
</p>

To interact with the LUT of an image, I will use a tool called [Fiji](https://imagej.net/software/fiji/). Let's look at this 8-bit image:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/parrots.gif" width=40%  height=40%></p>

Using Fiji, we can go to `Image > Color > Edit LUT` to see the following LUT:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/parrot-lut.png" width=30%  height=30%></p>

We can see 256 different colors (which makes sense since an 8-bit value can hold numbers 0-255). By changing the colors associated to any of the 256 values, we can change the colors that make up the image. 

Where is this going? Well what happens if we take an image and make all of the LUT colors the exact same, maybe black? Well then the entire image will be black and we will have no idea what the actual image is supposed to show, and thus we can hide a secret message. 

Let's say we're given the following image [lut-steg.tif](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/lut-steg.tif) and are tasked with finding the secret message: 

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/lut-steg-display.png" width=40%  height=40%><br>
    <em>github can't display the real image file properly, so this is just a screenshot of it, please downlaod the real file from this folder</em>
</p>

Opening it in Fiji and viewing the LUT, we see that it's all black.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/steg-lut.png" width=30%  height=30%></p>

If we click on the first LUT color value and change it to something that's not black, like red, we see the secret message.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/steg-lut-solved.png" width=40%  height=40%></p>

This is just one simple (and somewhat rare) method of hiding information in an image, there are plenty more. The goal was just to open your eyes to some different techniques that can be used for manipulating images. 

p.s. The tool `stegsolve` will be introduced in the next section, which has the functionality to set a random color map for an image. It will also make the secret message visible. You can try it out yourself. 


# Image Bit Planes
Hiding images in specific bit planes is a popular method of steganography. This method is very similar to LSB steg, in that it manipulates the values of the actual bits of a pixel. Each bit in an RGB byte is a part of a bit plane. The LSB would be bit plane 0. The next bit would be bit plane 1, and so on. This means that LSB steg is really just using getting information from one specific bit plane. Here is a visualization of the 8 bit planes in a greyscale image:

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/bit-planes.jpg" width=60%  height=60%><br>
    <em>source: https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/53189/versions/1/screenshot.jpg</em>
</p>

Various tools usually can help visualize these bit planes based on the color of the pixel. So red bit plane 0 would give you all of the bits in bit plane 0 for only the bytes coding for red of each pixel, and so on. There are two good tools for this: `stegsolve` (linux) and [stegonline](https://stegonline.georgeom.net/). Use the following commands to install and run stegsolve on linux:

```
wget http://www.caesum.com/handbook/Stegsolve.jar -O stegsolve.jar
chmod +x stegsolve.jar
./stegsolve.jar
```

Let's take a look at the following image [octogun-bit-plane.png](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/octogun-bit-plane.png) and see if we can find the flag by looking through the bit planes. I will be using [stegonline](https://stegonline.georgeom.net/) but `stegsolve` will work the exact same.

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG 200/octogun-bit-plane.png" width=40%  height=40%><br>
    <em>source: my incredible Paint3D skills (octogun-bit-plane.png)</em>
</p>

Here is what red bit plane 0 looks like:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/red-0.png" width=40%  height=40%></p>

Here is what red bit plane 2 looks like:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/red-2.png" width=40%  height=40%></p>

But if we look at red bit plane 1, we see the flag!

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/red-1-flag.png" width=40%  height=40%></p>

# Image XOR
Another method of hiding images in other images is performing a logic operation between the bits of the two images, such as an XOR (exclusive or). If you already know about XOR, feel free to skip this and the next paragraph. XOR (symbol is ⊕) compares two bits and returns `0` if they are equal and `1` if they are not. Here is a basic table to show this logic:

| x | y | x ⊕ y |
|:-:|:-:|:------:|
| 0 | 0 |   0    |
| 0 | 1 |   1    |
| 1 | 0 |   1    |
| 1 | 1 |   0    |

XOR is a very popular operation which you will encounter a lot, especially in cryptography. This is because it's copeletely reversible, so `x ⊕ y = z, x = y ⊕ z`. Try to verify this in your head using the table above. In relation to image steganography, this means that if you XOR your secret image with some random cover image and get an output image, you can get your secret image back by XORing the output image with the cover image (the cover image is acting like a key). In formula terms: `steg operation: key ⊕ message = output`, `unsteg operation: output ⊕ key = message`, in which `key` = cover image and `message` = secret image. I will not go into detail about uses of XOR in cryptography since it is discussed in the CRYPTO course.

Let's say we're given two files, the output of an image XOR operation [xor-steg.tif](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/xor-steg.tif) and the cover image used in the operation [xor-cover.jpg](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/xor-cover.jpg):

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/xor-steg-display.png" width=40%  height=40%><br>
    <em>xor-steg</em><br>
    <em>github can't display the real image file properly, so this is just a screenshot of it, please downlaod the real file from this folder</em>
</p>

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG 200/xor-cover.jpg" width=40%  height=40%><br>
    <em>xor-cover.jpg</em>
</p>

There are several ways you can XOR these, including using `imagemagick` on linux or using Fiji, as we did last time. I will show both methods here.

#### `Fiji`
1. open both files in Fiji
2. `Process > Image Calculator`
3. Select one image for `Image 1`, the other for `Image 2`, and set the `operation` to `XOR`. 
4. You should see the flag in the output image!

#### `imagemagick`
1. Install on linux
```
wget https://download.imagemagick.org/ImageMagick/download/binaries/magick (or download from browser, which is faster)
chmod +x magic 
```
2. run `./magic xor-cover.jpg xor-steg.tif -evaluate-sequence xor output`
3. You should see the flag in the output image!

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG 200/xor-secret.jpg" width=70%  height=70%><br>
    <em>secret image</em>
</p>

# Files Within Files
One popular method of hiding files is embedding them entirely within another. This topic overlaps heavily with that of forensics, so I will not be going over how it works here. You should head over to Forensics 100 to learn about it. I am only including this topic within Steganography because it is a popular steg challenge type.

To check if a file has any files embedded within it, you can use the linux tool `binwalk`. For example, let's say we're given [fileception-cover.png](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/fileception-cover.png) 

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG 200/fileception-cover.png" width=40%  height=40%></p>

Let's run `binwalk` against it:

```console
$ binwalk fileception-cover.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 1917 x 1078, 8-bit/color RGB, non-interlaced
41            0x29            Zlib compressed data, default compression
337629        0x526DD         PNG image, 1200 x 400, 8-bit/color RGBA, non-interlaced
```
We can see that it found a `PNG`, `Zlib compressed data`, and another `PNG`. We can safely ignore the `Zlib compressed data` as PNG's use zlib to compress the image datastream.  We are left with the fact that binwalk identified two different PNG images wihthin `fileception-cover.png`, so how do we extract them?

I usually stick to two main tools for extraction, `binwalk` and `foremost`. Basically if one doesn't work, I use the other.

### Extract with `binwalk`
__Syntax:__ `$ binwalk -e fileception-cover.png`<br>
__Output:__ directory called `_fileception-cover.png.extracted`<br>
If we look in that directory we don't see anything. There may be a way to adjust some binwalk options to make it work, but before wasting time on that, we can try `foremost`

### Extract with `foremost`
```console
$ foremost -v fileception-cover.png
Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus
Audit File

Foremost started at Wed Jun 16 21:58:57 2021
Invocation: foremost -v fileception-cover.png 
Output directory: /root/Documents/masoncc/myChals/output
Configuration file: /etc/foremost.conf
Processing: fileception-cover.png
|------------------------------------------------------------------
File: fileception-cover.png
Start: Wed Jun 16 21:58:57 2021
Length: 344 KB (352765 bytes)
 
Num	 Name (bs=512)	       Size	 File Offset	 Comment 

0:	00000000.png 	     329 KB 	          0 	  (1917 x 1078)
1:	00000659.png 	      14 KB 	     337629 	  (1200 x 400)
*|
Finish: Wed Jun 16 21:58:57 2021

2 FILES EXTRACTED
	
png:= 2
```
__Output:__ directory called `output`<br>
If we look in that direcotry, we see a subdirectory called `png`, which contains two files.
```console
$ ls output/png
00000000.png  00000659.png
```

Opening those two images, we see that `00000659.png` contains a secret message:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG 200/fileception-secret.png" width=40%  height=40%></p>

If you are interested in learning more about how this works and other use-cases, please head over to Forensics 100 which will be covering file carving and binwalk in more depth.

# Steghide
Finally, I will talk about one of the most common tools in steganography challenges, `steghide`. You can read how the tool works on their [manpage](http://steghide.sourceforge.net/documentation/manpage.php) since it's quite involved. All you really have to know is how to use it.

First thing to keep in mind is its supported file formats: `JPEG`, `BMP`, `WAV` and `AU`. This means that if you're solving a challenge and it isn't one of these file formats, you can elimitate this as a possible way to solve it.

### Embedding Files
```console
$ steghide embed -cf coverfile.jpeg -ef secretfile.jpeg -sf outputfile.jpeg -p secretpassword
```
*p.s. there are plenty of other options, just look at the help menu of steghide*

### Get Info 
Before attempting to extract anything, I like have `steghide` attempt to display info about the given file. With the correct password, it will give us useful information, including if there is an embedded file.

Let's look at [steghidden.jpeg](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/steghidden.jpeg):

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG 200/steghidden.jpeg" width=40%  height=40%></p>

Let's use the `steghide` `info` function to try and see if there is an embedded file.

```console
$ steghide info steghidden.jpeg                    
"steghidden.jpeg":
  format: jpeg
  capacity: 26.8 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase: 
```
We see that it asks for a password. Maybe we hope that no password is set, so we can just press "enter" (we can also provide the `-p` parameter to specify the password when running the initial command)
```console
steghide: could not extract any data with that passphrase!
```
Damn, no dice.

Let's pretend, for now, that we know the password from some hint in the challenge or that indeed there was no password set.

```console
$ steghide info steghidden.jpeg -p "secretpassword"                 
"steghidden.jpeg":
  format: jpeg
  capacity: 26.8 KB
  embedded file "flag.jpeg":
    size: 17.1 KB
    encrypted: rijndael-128, cbc
    compressed: yes
```

We see that there is an embedded file called `flag.jpeg`. 

### Extract Hidden File

```console
$ steghide extract -sf steghidden.jpeg -xf stegunhidden.jpeg -p "secretpassword"
wrote extracted data to "stegunhidden.jpeg".
```

Opening [stegunhidden.jpeg](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/stegunhidden.jpeg) we see:

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG 200/stegunhidden.jpeg" width=40%  height=40%></p>

But what if we hadn't known the password?

### Attempt Password Brute Force
If we don't know the password to use for `steghide`, we can use a tool called [stegbrute](https://github.com/R4yGM/stegbrute). I'm not sure if it's already pre-installed on kali, so if not, follow the installation instructions on the GitHub. `stegbrute` will take in a wordlist and try every entry as the password to `steghide`. This may take a while depending on the length of your wordlist and the number of threads you tell `stegbrute` to use.

```console
$ stegbrute -f steghidden.jpeg -w /usr/share/wordlists/rockyou.txt -t 10 -x stegunhidden.jpeg
============================================================
     ____  _             ____             _       
    / ___|| |_ ___  __ _| __ ) _ __ _   _| |_ ___ 
    \___ \| __/ _ \/ _` |  _ \| '__| | | | __/ _ \
     ___) | ||  __/ (_| | |_) | |  | |_| | ||  __/
    |____/ \__\___|\__, |____/|_|   \__,_|\__\___|
                   |___/                          

StegBrute v0.1.1 - By R4yan
https://github.com/R4yGM/StegBrute

exist
Bruteforcing the file 'steghidden.jpeg' with the wordlist '/usr/share/wordlists/rockyou.txt' using 10 threads

password try: secretpassword - Success 
File extracted!
Password: secretpassword
Results written in: stegunhidden.jpen
Tried passwords : 80999
Successfully cracked in 961.31s
============================================================
```

After about 80,999 password attempts and 16 minutes, it finally cracked it! Allocating more than 10 threads will probably speed up the process some, but it will still be a pretty slow process. Unless you're confident that the steg challenge wants you to use steghide to find a hidden file/brute force steghide, this may not be the way.