<h1 align="center">STEG 300</h1>
  <p align="center">
     Audio Steg
  </p>

### Table of contents

- [Introduction](#introduction)
- [Audio LSB](#audio-lsb)
- [Spectrograms](#spectrograms)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)


## Introduction
This will be a pretty short course because there is not too many unique aspects of audio steg when compared to image steg. The two topics we will cover are LSB steg in audio files and encoding secret images in audio spectrograms

## Audio LSB
Audio LSB steg is basically the same thing as LSB steg with images. You just replace the least-significant bit of each byte of data with your own. One nice tool that can do this for us is [WavSteg](https://github.com/ragibson/Steganography#WavSteg). You can also implement this using python, such as this code from @reachsumit: [sender.py](https://gist.github.com/reachsumit/5376441d341bb5c8b361a2f3e0798993) and [receiver.py](https://gist.github.com/reachsumit/583c76ffd740e1a952d65da3c676931f).

For our purposes, let's use [WavSteg](https://github.com/ragibson/Steganography#WavSteg). 

`WavSteg` requires us to tell it how many bytes to extract from a file and how many LSBs to use. If we don't know those values, we might just need to guess and check.

Given [lsb-steg.wav](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20300/lsb-steg.wav), let's first try only the first LSB and extracting just 500 bytes.

```console
$ stegolsb wavsteg -r -i lsb-steg.wav -n 1 -b 500 -o test.txt         
Files read                     in 0.00s
Recovered 500 bytes            in 0.00s
Written output file            in 0.00s
```
```console
$ cat test.txt              
flag{LSB_p2_electric_boogaloo}
�H�d�2́D�ɓ�}̙" $��������������o������������T���t���`4�Ub��<%.n��'��U)`ճ�G���J�)%y��"����1��I˸[_%eKc�2J�X��k��lc�M�p'     ��T
                                                                                                                          %%Y.�9JL������n
                                                                                                                                         3P��X����W�*2��6AGQ��
                                                                                                                                                              �%�T\�O��k����3Ƴ;�f�|!Ã�T���A��40����Z��CV���3�e�Y���o:�K�a-i�g1��g��<���e����U���.1���x4���z35�3f��0�RZ��yc                 
```

Who knew solving challenges was so easy, all you have to do is be the one who makes it.

## Spectrograms
Spectrograms are a visual representation of frequencies and amplitude over time. This is differnet from a normal waveform, which just shows amplitude over time. Here are two examples:

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/waveform.png" width=40%  height=40%><br>
    <em>waveform</em><br><em>source: https://www.izotope.com/en/learn/understanding-spectrograms.html</em>
</p>

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/spectrogram.png" width=40%  height=40%><br>
    <em>spectrogram</em><br><em>source: https://www.izotope.com/en/learn/understanding-spectrograms.html</em>
</p>

In the spectrogram, amplitutude is diplayed by brightness, the y-axis is frequency, and x-axis is time. In the waveform, amplitude is the y-axis and time is the x-axis.

If we think about it, this means we can almomst "draw" images as sound, and visualize them using spectrograms. Adjusting amplitude will increase brightness to make lines stand out. The range of frequencies will make the lines. And time gives us a 2D canvas to work with.

Two good and free ways to view the spectrograms of an audio file is using [sonic visualizer](https://www.sonicvisualiser.org/) and [audacity](https://www.audacityteam.org/) (which is pre-installed on Kali). 

Let's say we were given [spectrogram.wav](https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Steg/STEG%20300/spectrogram.wav):

If we want to try to view it in `Sonic Visualizer`, we have to open the file, then `pane > add spectrogram`. We see the flag!

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/sonic-visualizer.png" width=40%  height=40%></p>

If we want to view it in `Audacity`, we open the file, "open menu" with `Shift+M` and then click `Spectrogram`. By default it will only show frequencies up to 8kHz but we can change that. Either `open menu > spectrogram settings > increase the "Max Frequency"` or right click on the y-axis panel showing the frequencies and click `Zoom to Fit`. We see the flag!

<p align="center"><img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/steg/audacity.png" width=40%  height=40%></p>

(If your spectrogram looks different, aka red and hard to read, it's because I highlighted the audio track which makes it easier to read)

This is a pretty popular method used in audio steg CTF challenges, so make sure to check it. You might also be hinted to the fact that something is hidden in the spectrogram if you play the audio file and you hear strange frequencies and sounds that shouldn't be there.


## Practice:
- TCTF: TODO
- picoCTF: TODO
- TryHackMe: TODO

## More Resources:
- https://www.izotope.com/en/learn/understanding-spectrograms.html
- https://sumit-arora.medium.com/audio-steganography-the-art-of-hiding-secrets-within-earshot-part-1-of-2-6a3bbd706e15
- https://sumit-arora.medium.com/audio-steganography-the-art-of-hiding-secrets-within-earshot-part-2-of-2-c76b1be719b3


## Creators

**Daniel Getter**

Enjoy :metal: