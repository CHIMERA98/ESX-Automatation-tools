# ESX-Automatation-tools
GUI tools to automate ESX environments

# Auto Turn on

## Introduction

This tool allows users to automatically turn on all VMs on a certain ESX server under the folder "<username>_turnon_folder" (and sub-folders recoursively).

## Usge

```
TurnOESX.exe [-u <username>] [-p <password>] [-s server]
```

Or:

```
python TurnOESX.py [-u <username>] [-p <password>] [-s server]
```

If no password is provided with "-p", the script will prompt the user with a small window to enter credentials.

## Depndencies

### For the python version:

1. pyVmomi

2. pyVim

### For the executable:

No dependencies :)
