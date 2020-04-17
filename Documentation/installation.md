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
2. The output of `voyager config` should indicate where to find the config file
3. Open the config file in a text editor
4. Get your Artifactory API key
    1. Go to your Artifactory `Edit Profile` page [link](https://artifactory.prodrive.nl/artifactory/webapp/#/profile)
    (click on your name on the top right side of the Artifactory webpage)
    2. Enter your password and press `Unlock`
    3. Generate and copy your API key
5. Fill in you API key in the between the empty quotes in the config file
6. Save the config file
7. Run `voyager config` again. It should print the contents of the config file