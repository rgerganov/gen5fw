# Overview
This repo contains tools and instructions how to patch and deploy the Standard-class 
Gen5 Navigation firmware running on the head unit of some Hyundai, KIA and Genesis cars.

![gen5](/pics/gen5.png "Standard-class Gen5 Navigation")

**WARNING: Make sure you follow the exact steps below or you may risk to brick your car's head unit**

# Installation
The main tool `gen5.py` is written in Python3. You can install its dependencies (preferrably into venv) with `pip`:
```
 pip install -r requirements.txt
```
You will also need the Android tools for manipulating sparse images:
```
 sudo apt install android-sdk-libsparse-utils
```

# Obtaining firmware

Download the latest firmware for your car using the Navigation Updater app from [Hyundai](https://update.hyundai.com/)/[KIA](https://update.kia.com/)/[Genesis](https://update.genesis.com/).
The Navigation Updater will prepare a USB drive or SD card with the firmware.
Then install the firmware on your car using the standard update mechanism.
Do *not* proceed with the next steps if the official firmware cannot be installed successfully on the car.

# Patching
This guide shows how to patch the official firmware to enable ADB but you are free to change whatever you want.

Take `update_package.zip` from the downloaded firmware and crack its password using the methods described in this [blog post](https://xakcop.com/post/hyundai-hack/). After unzip, you will get `update.zip` and `otacerts.zip`:
```
$ unzip update_package.zip 
Archive:  update_package.zip
[update_package.zip] update.zip password: 
 extracting: update.zip              
 extracting: otacerts.zip            

```
Create a new directory `fw` and extract `update.zip` there:
```
$ mkdir fw
$ cd fw
$ unzip update.zip 
Archive:  update.zip
signed by SignApk
  inflating: META-INF/com/google/android/update-binary  
  inflating: META-INF/com/google/android/updater-script  
  inflating: boot.img                
  inflating: lk.rom                  
  inflating: recovery.img            
  inflating: res/keys                
  inflating: romcopy/dram.rom        
  inflating: romcopy/emmc_header.rom  
  inflating: romcopy/padding.img     
  inflating: splash.img              
  inflating: system.ext4             
  inflating: META-INF/com/android/otacert  
  inflating: META-INF/MANIFEST.MF    
  inflating: META-INF/CERT.SF        
  inflating: META-INF/CERT.RSA       
```
`system.ext4` contains the root file system of the head unit. Mount it like this:

```
$ mkdir /tmp/car
$ sudo mount system.ext4 /tmp/car
```
Now we can edit the mounted file system in `/tmp/car`.
For example we can delete the `adb_hide` feature in `/etc/permissions/com.hkmc.software.engineermode.adb_hide.xml` and thus enable ADB:
```
$ sudo vim /tmp/car/etc/permissions/com.hkmc.software.engineermode.adb_hide.xml
$ cat /tmp/car/etc/permissions/com.hkmc.software.engineermode.adb_hide.xml
<permissions>
</permissions>
```
When done, unmount the file system:
```
$ sudo umount /tmp/car
```
Convert the patched `system.ext4` to sparse image using the `img2simg` tool:
```
$ img2simg system.ext4 system.img
```
Finally, encrypt all files using `gen5.py encrypt`:
```
$ cd ..
$ ./gen5.py encrypt fw security_force
```
The first parameter is the `fw` directory which contains the modified firmware.
The second parameter is the output directory where encrypted files will be written.
The name of the output directory must be always `security_force`.
Verify that you have 7 files there:
```
$ ls security_force 
encrypt_boot.img  encrypt_lk.rom  encrypt_partition.dat  encrypt_recovery.img  encrypt_splash.img  encrypt_system.img  file_info
```
Copy the `security_force` directory on a USB drive formatted with FAT32.
  
# Deploy
There is a secret recovery mechanism which is used for installing encrypted firmware on the head unit.
Before plugging the USB drive with the patched firmware, make sure this mechanism is available.
Press and hold POWER (left knob) and MAP buttons on your head unit and then power on:

![head_unit](/pics/head_unit.jpg "Head unit")

On some head units the buttons are POWER+HOME. You can also hold the buttons and reset the unit with a toothpick.
You should get an error similar to this one:

![uboot](/pics/uboot.jpg "u-boot")

Now plug the USB drive and reset the unit while holding POWER+MAP. The update process should begin.

# Enable ADB

Once the update is complete, you can enable ADB in the Engineering Mode.
This year's password for the Engineering Mode is "2603".
Go to the "Module Info" and open the third page. Tap 5 times in the bottom right corner. The ADB settings should appear:

![adb](/pics/adb.jpg "adb")

## root shell

You can get root shell by running the `/bin/amossu` binary from the `adb` shell. This binary is part of the official firmware:
```sh
$ ls -la bin/amossu
-rwsr-sr-x 1 root root 37216 Oct  6 08:29 bin/amossu
```
It has the setuid bit enabled and it simply does:
```c
setgid(0);
setuid(0);
execv("/system/bin/sh",__argv);
```

# Feedback

Let me know if you come up with some cool mods using the hack!
The ultimate goal would be to run Doom on the head unit :)

