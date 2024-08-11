# Omni-Manager
Omni-Manager is a cross-platform software management tool that provides an intuitive graphical user interface (GUI) for installing, updating, and upgrading software packages on Linux, macOS, and Windows. It aims for high system compatibility by supporting a wide range of package managers across different operating systems. Omni-Manager automatically detects the operating system and manages the installation of necessary package managers if they are not already installed.

## Features
Cross-platform compatibility: Supports Linux, macOS, and Windows. The perfect utility to throw onto a removable drive when managing multiple machines running different operating systems.

## Automatic package manager installation:

Installs Homebrew on macOS if not already installed.

Installs Chocolatey on Windows if not already installed.

Search functionality: Search for software packages across multiple package managers.

Batch installation: Install multiple software packages simultaneously.

Update and upgrade options: Update and upgrade all installed software packages with a single click.

Automatic OS detection: Automatically detects the operating system to provide the appropriate options.

Sudo password handling: Prompts for the sudo password on Linux and macOS when necessary.

UAC handling: Automatically triggers the UAC prompt on Windows for elevated privileges.

Wide package manager compatibility: Supports the following package managers:

## Linux:
APT (Advanced Package Tool)
DNF (Dandified YUM)
Pacman (Arch Linux package manager)
Flatpak
Zypper (openSUSE package manager)
Yum (Yellowdog Updater, Modified)
Snap
Guix (GNU package manager)

## macOS:
Homebrew

## Windows:
Chocolatey

## Prerequisites
Ensure that Python 3.x is installed on your system. You can download it from python.org.

## Run the application:
On any OS, run the application by executing:

`python3 omni_manager.py`

`python omni_manager.py`

Note: ensure the path to the program is correct

# Usage

## Starting the Application

Launch the Omni-Manager by running the Python script as mentioned above.
The application window will display the detected operating system and present options to search for and install software packages.

## Searching for Software

Enter the name of the software package you want to search for in the "Enter Program Name(s)" field.
Click the Search button.
A new window will appear with a list of search results. You can navigate through the results using the Next Page and Previous Page buttons.
Select the desired software from the list and click Select.

## Installing Software

After selecting the software, click the Install button.

## For Linux/macOS:
If the installation requires sudo privileges, a password prompt will appear.

## For Windows:
The program will trigger a UAC prompt for elevated privileges.

## Updating/Upgrading Software
Check the Update All or Upgrade All checkboxes to update or upgrade all installed software packages, respectively.
Click the Install button to execute the update/upgrade process.

## Troubleshooting
Failed Installations: If an installation fails, an error message will appear with details. Ensure that your internet connection is active and that the package manager is functioning correctly.
Permissions Issues: On Linux/macOS, ensure you have sudo privileges. On Windows, ensure that you allow the UAC prompt to proceed.

## Acknowledgements
This tool uses the tkinter library for the GUI and leverages package managers like APT, Yum, Pacman, Homebrew, and Chocolatey for software management.
