# Installation

## Windows
For Windows we provide standard installers that will install voyager into AppData and set up your `PATH` variable.

1. Uninstall previous versions of voyager first
1. Download the latest version of the installer from the releases page.
2. Run the installer
3. Go to the next page to view the instructions for connecting to your Artifactory instance

### Git bash
If you're planning to use voyager within git bash it is needed to run through winpty. 
Otherwise `voyager login` and text highlighting don't work.
Please run the following code to add an alias to your `.bashrc` file:
```Bash
echo "alias voyager='winpty voyager'" >> ~/.bashrc
```

## Linux
For Linux we provide compiled executables with pyinstaller. If there is a system mismatch you may need to build voyager yourself.
For installation in Linux run the following commands in the shell

1. `mkdir -p ~/voyager`
1. `cd ~/voyager`
1. Download voyager into this folder
1. `chmod +x ./voyager`
1. `echo "export PATH=\$PATH:$(pwd)" >> ~/.profile`
1. Go to the next page to view the instructions for connecting to your Artifactory instance

## Building from scratch
In case your platform does not match any of the provided binaries it is easy to build voyager into an executable. For all the python commands below it is assumed that Python 3.7 is used.

1. Clone the repository
1. `python -m venv env`
1. Activate the virtual env
1. `pip install -r requirements.txt`
1. `pyinstaller deploy/voyager_onefile.spec`
1. The onefile executable can be slow on Windows, it that's the case try `pyinstaller deploy/voyager.spec`
1. Executables can be found in the dist folder