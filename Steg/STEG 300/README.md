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


# Introduction
This will be a pretty short course because there is not too many unique aspects of audio steg when compared to image steg. The two topics we will cover are LSB steg in audio files and encoding secret images in audio spectrograms

# Audio LSB
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

Wow, we must be so lucky since I definitely didn't choose those numbers because I was the one that encoded it...