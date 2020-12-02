# Dishita-Midha-MRM

Ubuntu Installation:
-----
1) Disable fast startup
2) Disable secure boot via advanced startup
3) Create disk partition in disk mngmt ( 80 gb ssd for Ubuntu)
4) Download Ubuntu 18.04 and etcher.io
5) Flash pen drive with help of etcher.io
6) Restart while pressing f12 
7) Choose try without installing
8) Select "something else"
9) Create 20gb for / , 6.5 gb for /swap, rest for /home
10) Click on install third party drivers

Issues encountered during installation : NONE

Issues encountered post installation : Touchpad doesn't work in ubuntu (works in windows)

Attempt to fix the issue: In terminal,

                         (to check for presence of touchpad) less /proc/bus/input/devices ----> list of input devices ----> touchpad not in list
                         
                         (solution as suggested in stackoverflow) 1.sudo nano /etc/default/grub 
                                                                  2. modify GRUB_CMDLINE_LINUX_DEFAULT = "quiet splash" with GRUB_CMDLINE_LINUX_DEFAULT = "i8042.reset quiet splash" 
                                                                  3. save and sudo upgrade-grub
                                                                  4. reboot ----> touchpad still not working
Status: UNRESOLVED


Python2.7 installation
-----

sudo apt update

sudo apt upgrade

sudo apt install python2.7

sudo apt install python-pip

Issues encountered: NONE

Jupyter notebook via pip installation
-----
sudo pip install --upgrade pip

sudo pip install --upgrade jupyter

jupter notebook: installed

Issues encountered: NONE


VScode Installation
------
1.Download VScode installer(.deb) from https://code.visualstudio.com/download

2. In terminal, cd Downloads/

                ls 
                
                sudo dpkg -i <installer file name>
                
VScode installed 

Issues encountered: NONE
                





                                                                
