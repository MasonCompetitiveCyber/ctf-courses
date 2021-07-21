<h1 align="center">LINUX 100</h1>
  <p align="center">
     Kali Linux and VMware 
  </p>

### Table of contents

- [Introduction](#introduction)
- [Installing VMware Workstation Pro](#installing-vmware-workstation-pro)
- [Installing Kali Linux](#installing-kali-linux)
- [Bonus Steps](#bonus-steps)
- [Creators](#creators)


## Introduction
This course will walk you through getting a Linux virtual machine onto your machine with VMware Workstation Pro. Having a Linux VM and knowing how to use Linux is necessary in this field. For this course, we will be installing a Linux operating system called Kali Linux and we will be running it with VMware. If you have not yet heard of Kali Linux, it is a Linux distribution that is tailor-made for cybersecurity-related tasks. It comes with many tools pre-installed that are meant for cyber so you don't have to. There are other Linux distributions you can use as well, such as Parrot, Ubuntu, and others.

We will be using VMware to run our virtual machine, but if you want to, some people prefer to use Virtual Box instead. 

## Installing VMware Workstation Pro
As students, we are given access to install the Pro version of VMware Workstation, which is great! If you want to use VirtualBox instead, you will have to google/youtube some tutorials. 

1. Go to https://e5.onthehub.com/WebStore/Security/SignIn.aspx?ws=57245579-6f24-de11-a497-0030485a8df0
   - If you haven’t registered yet, click Register in the top right. If you’ve already registered, login with your username@gmu.edu.
   - NOTE: Your username is your NETID@gmu.edu, NOT your NETID@masonlive.gmu.edu email address.
   - NOTE: Your password is NOT your GMU email or PatriotWeb password. If you don’t know your password, click “Forgot Username or Password.”
2. Select the correct VMware product. Choose `VMware Workstation 16.x Pro` if you are using Windows and  `VMware Fusion 12.x Pro` if you are using Mac.
<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/linux/vmware-selection.png" width=75%  height=75%><br>
</p>

3. Add the product to your cart and checkout. You should see a product key. Save that somewhere (like copy/paste it into notepad) as you will need it later. Now press the Download button (sorry I don't have screenshots for this as I am not allowed to check out again since I have already done so before).
4. Now you can follow any guide online about how to follow the install/setup process. For Windows users, here's a good one (starting at Step 3): https://www.educba.com/install-vmware/. There are plenty of YouTube videos as well that do a good job at walking you through these steps.
5. At this point you should have VMware Workstation Pro ready to go! If you don't and are having trouble, feel free to reach out to us for help. 

## Installing Kali Linux
1. If you don't already have it, install 7zip (https://www.7-zip.org/download.html)
2. Go to https://www.kali.org/get-kali/#kali-virtual-machines and click on the VMware downoad. You should get a large .7z file
3. Use 7zip to unzip the file
<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/linux/7zip.png" width=60%  height=60%><br>
</p>

4. You should no have the unzipped folder that has the following contents. You should move this folder to a location where you want to keep your VMs. VMware will default to creating VMs in a "Virtual Machines" folder it will place in your "Documents" folder (if you end up making VMs from .iso files. You don't really need to worry about this because you can change that location too). I just make my own "VMs" folder to put them in. 
<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/linux/unzipped.png" width=50%  height=50%><br>
</p>

5. You should see a `.vmx` file somewhere near the top. Right click on it and open it with VMware Workstation 
<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/linux/vmx.png" width=60%  height=60%><br>
</p>

6. Now you can power on the VM. If you get a pop-up right away, just press "I Copied It"
7.  On the login screen, the default username is `kali` and the password is `kali`. 
8.  You're in!

## Bonus Steps
- Configure a shared folder so you can share files between your virtual machine and your host
  - here's a good video: https://www.youtube.com/watch?v=bUDup4RibEs&ab_channel=VonnieHudson
  - google is your friend
  - if you can't get it working, reach out to us
- Edit the virtual machine settings
  - Press "Edit virtual machine settings"
  - Set the settings however you would like depending on the laptop/computer you are running on. 2GB of memory should be enough, but if you have enough to spare, bumping it up to 4GB would be nice. You can also increase/decrease the # of processors and Hard Disk space as well if you want to 
<p align="center">
    <img src="https://github.com/MasonCompetitiveCyber/ctf-courses/raw/main/images/linux/first-open.png" width=85%  height=85%><br>
</p>

## Creators

**Daniel Getter**

Enjoy :metal:
