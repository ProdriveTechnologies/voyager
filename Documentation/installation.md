---
title: "Installation"
weight: 10
---
# Installation

## Windows

### Installer

1. Download the latest version of the installer from [artifactory](https://artifactory.prodrive.nl/artifactory/siatd-generic-local/Tools/Installer).
2. Run the installer and select Voyager in the GUI.
3. Log off and on again to process changes in the Windows registry.

### Manual installation

1. Download the latest version from [Artifactory](https://artifactory.prodrive.nl/artifactory/webapp/#/artifacts/browse/tree/General/siatd-generic-local/Tools/voyager)
    1. Please note that the onefile versions are meant for CI (They start slower)
2. Extract the zip file and place contents in `C:\voyager`
3. Add `C:\voyager` to the PATH variable
    1. Go to start and type `Edit environment variables for your account`
    2. In the User variables section select `Path` and click `Edit...`
    3. Add a `New` entry with the contents `C:\voyager`
    4. Click `Ok` and again `Ok` to save

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