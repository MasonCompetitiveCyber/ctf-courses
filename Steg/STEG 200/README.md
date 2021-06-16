<h1 align="center">STEG 200</h1>
  <p align="center">
     More Image Steg and Audio Steg
  </p>

### Table of contents

- [Introduction](#introduction)
- [Image LUT](#image-lut)
- [Bit Planes](#image-bit-planes)
- [XOR](#image-xor)

- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

# Introduction
In this course, we will continue talking about methods of image steganography and introduce methods of audio steganography. For image steg, we will talk about: LUT, bit planes, XOR, embedded files. For audio steg, we will talk about LSB, and spectrograms/sonic visualizers. There are almost an infinite amount of ways to hide information, so it's not feasible to go through all of them, but at least these should cover basic CTF steg problems.

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

Let's say we're given the following image and are tasked with finding the secret message: 

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20200/lut-steg.gif" width=40%  height=40%><br>
    <em>lut-steg.tif</em>
</p>

Opening it in Fiji and viewing the LUT, we see that it's all black.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/steg-lut.png" width=40%  height=40%></p>

If we click on the first LUT color value and change it to something that's not black, like red, we see the secret message.

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/steg-lut-solved.png" width=40%  height=40%></p>

This is just one simple (and somewhat rare) method of hiding information in an image, there are plenty more. The goal was just to open your eyes to some different techniques that can be used for manipulating images. 

p.s. The tool `stegsolve` will be introduced in the next section, which has the functionality to set a random color map for an image. It will also make the secret message visible. You can try it out yourself. 


# Image Bit Planes
Hiding images in specific bit planes is a popular method of steganography. This method is very similar to LSB steg, in that it manipulates the values of the actual bits of a pixel. Each bit in an RGB byte is a part of a bit plane. The LSB would be bit plane 0. The next bit would be bit plane 1, and so on. This means that LSB steg is really just using getting information from one specific bit plane. Here is a visualization of the 8 bit planes in a greyscale image:

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/bit-planes.jpg" width=40%  height=40%><br>
    <em>source: https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/submissions/53189/versions/1/screenshot.jpg</em>
</p>

Various tools usually can help visualize these bit planes based on the color of the pixel. So red bit plane 0 would give you all of the bits in bit plane 0 for only the bytes coding for red of each pixel, and so on. There are two good tools for this: `stegsolve` (linux) and [stegonline](https://stegonline.georgeom.net/). Use the following commands to install and run stegsolve on linux:

```bash
wget http://www.caesum.com/handbook/Stegsolve.jar -O stegsolve.jar
chmod +x stegsolve.jar
./stegsolve.jar
```

Let's take a look at the following image and see if we can find the flag by looking through the bit planes. I will be using [stegonline](https://stegonline.georgeom.net/) but `stegsolve` will work the exact same.

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/steg/STEG 200/octogun-bit-plane.png" width=40%  height=40%><br>
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

Let's say we're given two files, the output of an image XOR operation and the cover image used in the operation:

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/steg/STEG 200/xor-steg.gif" width=40%  height=40%><br>
    <em>XOR output</em>
</p>

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/steg/STEG 200/xor-cover.jpg" width=40%  height=40%><br>
    <em>cover image</em>
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
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/steg/STEG 200/xor-secret.jpg" width=40%  height=40%><br>
    <em>secret image</em>
</p>
