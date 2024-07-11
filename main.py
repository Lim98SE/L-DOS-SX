#!/bin/python3
import os
import shlex as shell
import json
import sys
import hashlib

def redownload_system():
    import requests
    import tarfile

    system_image = requests.get("https://www.lim95.com/static/ldsx/system.tar")

    with open("sys.tar", "wb") as file:
        file.write(system_image.content)

    print("Unzipping image...")

    with tarfile.open("sys.tar") as file:
        file.extractall()

print("Loading L-DOS SX...")

print("Checking dependencies...")

try:
    import requests

except ImportError:
    print("Installing requests")
    os.system("python -m pip install requests")

try:
    import colorama
    colorama.init()

except ImportError:
    print("Installing colorama")
    os.system("python -m pip install colorama")

try:
    import threading

except ImportError:
    print("Installing threading")
    os.system("python -m pip install psutil")

print("Checking system file integrity...")
integrity_list = [
    "system/cmdint.py",
    "system/helpfile.lds",
    "system/packages/update.py",
    "system/packages/pkgman.py"
    ]

for i in integrity_list:
    try:
        open(i).close()

    except FileNotFoundError:
        print(f"[ldsx]/{i} not found. Downloading system image...")
        redownload_system()
        break

print("Loading config...")
try:
    with open("system/reg.ldr") as file:
        registry = json.load(file)

except (FileNotFoundError, json.decoder.JSONDecodeError):
    print("An error occured, recreating config...")
    with open("system/reg.ldr", "w") as file:
        registry = {
            "useColor": True,
            "prompt": "$ ",
            "password": None
            }

        json.dump(registry, file)

print("Checking paths...")

try:
    with open("system/path.lds") as file:
        pkg_paths = json.load(file)

except (FileNotFoundError, json.decoder.JSONDecodeError):
    print("An error occured loading paths, reverting to default...")
    pkgpath = f"{os.getcwd()}/system/packages"
    pkg_paths = [pkgpath]

    with open("system/path.lds", "w") as file:
        json.dump(pkg_paths, file)

home = os.getcwd()
error_paths = []

for i in pkg_paths:
    try:
        os.chdir(i)

    except FileNotFoundError:
        error_paths.append(i)

os.chdir(home)
if len(error_paths) == 0:
    print("No errors found in paths.")

else:
    for i in error_paths:
        pkg_paths.remove(i)

    with open("system/path.lds", "w") as file:
        json.dump(pkg_paths, file)

    print(f"Removed {len(error_paths)} errors from paths")

print("Loading command interpreter...")
with open("system/cmdint.py") as file:
    cmdint = file.read()

sysdir = f"{os.getcwd()}/system"

if registry["password"] != None:
    passwordIsCorrect = False

    while not passwordIsCorrect:
        passwordAttempt = input("Password: ")
        passwordHash = hashlib.md5(passwordAttempt.encode("utf-8")).hexdigest()

        if passwordHash == registry["password"]:
            passwordIsCorrect = True
            break

        print("Incorrect password. Try again.")

exec(cmdint)

if os.path.exists("system/autoexec.ldc"):
    print("Running autoexec...")
    with open("system/autoexec.ldc") as file:
        autoexec = file.readlines()

    for i in autoexec:
        if len(i.strip()) == 0: continue
        if shell.split(i)[0] != "#":
            handle(i)

running = True
while running:
    try:
        handle(input(registry["prompt"]))

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)

sys.exit(0)
