---
title: "Installation"
weight: 10
---
# Installation

## Windows

### Installer

1. Uninstall previous versions of voyager first
1. Download the latest version of the installer from [artifactory](https://artifactory.prodrive.nl:443/artifactory/siatd-generic-local/Tools/voyager/latest/win-setup/voyagerSetup.exe).
2. Run the installer
3. If this is your first time using voyager, please follow the steps in the `First time configuration` section below

### Git bash
If you're planning to use voyager within git bash it is needed to run through winpty. 
Otherwise `voyager login` and text highlighting don't work.
Please run the following code to add an alias to your `.bashrc` file:
```shell script
echo "alias voyager='winpty voyager'" >> ~/.bashrc
```

## Linux
For installation in Linux run the following commands in the shell

1. `mkdir -p ~/voyager`
1. `cd ~/voyager`
1. ``wget --user=`whoami` --ask-password https://artifactory.prodrive.nl/artifactory/siatd-generic-local/Tools/voyager/latest/linux-onefile/voyager``
1. `chmod +x ./voyager`
1. `echo "export PATH=\$PATH:$(pwd)" >> ~/.profile`
1. Follow the steps in the First time configuration chapter
1. Update the config file with the correct `default_arch` items for Linux

## First time configuration
1. Open a command prompt and run `voyager config` to generate the default config file
2. Next run `voyager login` and enter your password when prompted
3. Run `voyager config` again to view the contents of the config file