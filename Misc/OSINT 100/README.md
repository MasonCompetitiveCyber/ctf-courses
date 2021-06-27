<h1 align="center">OSINT 100</h1>
  <p align="center">
     Open-Source Intelligence Basics
  </p>

### Table of contents

- [Introduction](#introduction)
- [CTF Challenge Methodology](#ctf-challenge-methodology)
- [Tools](#tools)
- [Practice](#practice)
- [More Resources](#more-resources)
- [Creators](#creators)

## Introduction
OSINT, or Open-Source Intelligence, is the act of using publicly available (otherwise known as open-source) information to gain insight about a specific objectives. Using social media platforms, the internet, media, photos, journals, etc. to glean information about an objective would fall under the category of OSINT because the information being compiled and analyzed from these resources is publicly available. Businesses can use OSINT to track brand popularity, monitor market trends, and glean information about their competitors. Law enforcement and intelligence agencies may use OSINT to track or keep tabs on people of interest. Hackers could use OSINT to find potential non-technical weaknesses and vulnerabilities in a target. For example, they can launch a social engineering campaing against a high-level employee using information they posted on their social media. Useful info could be names of friends and family, date and location of birth, favorite vacation spot, or really anything that can paint a unique picture of a target. Since people may use family names, birthdates, hobbies, or locations in their passwords, hackers may use that information to create a password list unique to their target in hopes of increasing their chances to crack it.

## CTF Challenge Methodology
There is really only a limited amount of different challenges you will encounter in OSINT CTF challenges. You'll mostly see things related to finding a georgraphic location or some unique user information. Your most common tools would include searching through social media, google maps, reverse image search, historical records, and google. Because of this, there is really not *that* much to teach. The difficulty in OSINT challenges comes from the fact that you are given very little informaiton. You have to find what details are important and which aren't, so you will end up diving through time-wasting rabbit holes before you find the solution, if you even do. 

## Tools
I don't really have any OSINT challenges on hand to show (other than ones from CTFs that don't want write-ups at the moment) and it's not too easy to make them quicky, so the most I can do for you for now is provide a list of some useful tools that will help you search for relevant information.

**Reverse Image Search**
- http://images.google.com
- https://yandex.com/images/
- [Google Lens](https://lens.google/#!#download)
    - Example challenge: What is this building?

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/Misc/OSINT%20100/google-lens-chal.png" width=40%  height=40%><br>
    <em>google-lens-chal.png</em>
</p>

Now just pull up Google Lens on your phone and take a picture of the image. It may take a little finagling before it finally recognizes it.

<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/osint/google-lens-screenshot.png" width=40%  height=40%><br>
    <em>screenshot of me using google lens to solve this challenge</em>
</p>

**Image Metadata**
- `exiftool` (linux tool)
- [`metagoofil`](https://github.com/kurobeats/metagoofil) (linux tool)
- http://exif.regex.info/exif.cgi

**Username Search**
- http://hunter.io
- `sherlock` (linux tool)
- https://checkusernames.com/
- https://usersearch.org/index.php
- https://namecheckup.com/

**DNS**
- `whois` (linux tool)
- https://lookup.icann.org/lookup
- https://dnsdumpster.com/

**Company/Domain**
- [`theHarvester`](https://github.com/laramies/theHarvester) (linux tool) 
- [`sublist3r`](https://github.com/aboul3la/Sublist3r) (linux tool)

**Git**
- [`git-dumper`](https://github.com/arthaud/git-dumper) (linux tool)
- [GitTools](https://github.com/internetwache/GitTools) (linux tool)

**Automated/Swiss Army Knife**
- [`spiderfoot`](https://github.com/smicallef/spiderfoot?ref=d) (linux tool)
- [`reconspider`](https://github.com/bhavsec/reconspider) (linux tool)

**Other**
- https://www.shodan.io/
    - Please be careful on here, you can quite easily click on a malicious endpoint or honeypot. On the other hand, you can also quite easily use default passwords to get into stuff. Please make sure you are not doing anything illegal when using shodan. I had logged in to 2 different endpoints using default admin creds without thinking it would work the first time I went on Shodan. Luckily, they weren't anything serious or I could have been in some trouble, so please be careful and make smart decisions.


There are so many more tools out there, so I will link to a couple lists. What you may want to do is install the [Trace Labs OSINT VM ](https://www.tracelabs.org/initiatives/osint-vm#downloads). Instructions [here](https://download.tracelabs.org/Trace-Labs-OSINT-VM-Installation-Guide-v2.pdf). It contains basically any OSINT tool you would need and sorts all web-based tools in a bookmark in firefox, so it's super easy to use. The OSINT category of CTF challenges requires you to think creatively and be persistent, which is something I can't really show you here. You do not need basically any prerequisite knowledge to solve the challenges other than knowing some of these useful tools that can help.

## Practice:
- TCTF: TODO
- picoCTF: TODO
- TryHackMe: 
    - https://tryhackme.com/room/ohsint
    - https://tryhackme.com/room/sakura
    - https://tryhackme.com/room/somesint


## More Resources
- https://github.com/digitaldisarray/OSINT-Tools
- https://github.com/jivoi/awesome-osint

## Creators

**Daniel Getter**

Enjoy :metal: