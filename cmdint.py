def call_error(error):
    if registry["useColor"]:
        print(f"{colorama.Fore.RED}{error}{colorama.Style.RESET_ALL}")

    else:
        print(error)

def handle(command):
    if len(command) == 0:
        call_error("No command specified")
        return

    try:
        full_cmd = command
        args = shell.split(command)[1:]
        command = shell.split(command)[0].lower().strip()

    except ValueError:
        call_error("Misshapen command. Try again.")
        return

    validCommand = False

    match command:
        case "echo":
            print(" ".join(args))

        case "ls":
            path = os.getcwd()

            try:
                path = args[0]
                print(path)

            except:
                path = os.getcwd()

            try:
                os.listdir(path)

            except NotADirectoryError:
                call_error("Not a directory.")
                return

            for i in os.listdir(path):
                if registry["useColor"]:
                    if os.path.isdir(path + "\\" + i):
                        print(f"{colorama.Fore.GREEN}[DIR] {i}{colorama.Style.RESET_ALL}")

                    elif os.path.isfile(path + "\\" + i):
                        print(f"{colorama.Fore.BLUE}{i}{colorama.Style.RESET_ALL}")

                    elif os.path.islink(path + "\\" + i):
                        print(f"{colorama.Fore.RED}[SYM] {i}{colorama.Style.RESET_ALL}")

                    elif os.path.ismount(path + "\\" + i):
                        print(f"{colorama.Fore.YELLOW}[MNT] {i}{colorama.Style.RESET_ALL}")

                else:
                    if os.path.isdir(path + "\\" + i):
                        print(f"[DIR] {i}")

                    elif os.path.isfile(path + "\\" + i):
                        print(f"{i}")

                    elif os.path.islink(path + "\\" + i):
                        print(f"[SYM] {i}")

                    elif os.path.ismount(path + "\\" + i):
                        print(f"[MNT] {i}")

        case "cd":
            try:
                to = args[0].strip()

                if to == "~" and "~" not in os.listdir():
                    to = home

                os.chdir(to)

            except FileNotFoundError:
                call_error("Directory not found.")

            except IndexError:
                call_error("No arguments provided.")

        case "exit":
            global running
            running = False

        case "path":
            global pkg_paths

            try:
                args[0]

            except IndexError:
                call_error("No arguments provided. Try \"path help\".")
                return

            path_cmd = args[0].lower().strip()

            if path_cmd == "help":
                print("""
Paths are where your extra commands are stored. Run \"path list\" to see them.
You can also do \"path add\" and \"path remove\" to add and remove paths.
The pathfile is stored at \"(L-DOS SX folder)\\system\\path.lds\".

Example: path add C:\\
""".strip())

            elif path_cmd == "list":
                for i in pkg_paths:
                    print(i)

            elif path_cmd == "add":
                try:
                    args[1]

                except IndexError:
                    call_error("More arguments need to be provided.")
                    return

                pathToAdd = os.path.abspath(args[1]).strip()
                currentDir = os.getcwd()

                try:
                    os.chdir(pathToAdd)

                except FileNotFoundError:
                    call_error(f"{pathToAdd} not found.")
                    return

                os.chdir(currentDir)
                pkg_paths.append(pathToAdd)

                with open(f"{sysdir}\\path.lds", "w") as file:
                    json.dump(pkg_paths, file)

                if registry["useColor"]:
                    print(f"{colorama.Fore.GREEN}Added!{colorama.Style.RESET_ALL}")

                else:
                    print("Added!")

            elif path_cmd == "remove":
                try:
                    args[1]

                except IndexError:
                    call_error("More arguments need to be provided.")
                    return

                pathToRemove = args[1].strip()

                try:
                    pkg_paths.remove(pathToRemove)

                except ValueError:
                    call_error(f"{pathToRemove} not in paths.")
                    return

                if registry["useColor"]:
                    print(f"{colorama.Fore.GREEN}Removed!{colorama.Style.RESET_ALL}")

                else:
                    print("Removed!")

                with open(f"{sysdir}\\path.lds", "w") as file:
                    json.dump(pkg_paths, file)

        case "help":
            with open(f"{sysdir}\\helpfile.lds") as file:
                helpfile = file.readlines()

            try:
                helpcmd = args[0].strip().lower()

            except:
                helpcmd = ""

            found_helpfiles = 0

            for i in helpfile:
                if helpcmd == i.split()[0].strip().replace(":", ""):
                    print(" ".join(i.split()[1:]))
                    found_helpfiles += 1

            if helpcmd == "":
                for i in helpfile:
                    print(i.strip())
                    found_helpfiles += 1

            if found_helpfiles == 0:
                call_error(f"No help available for {helpcmd}.")

        case "ver":
            print("v1.0")

        case "passwd":
            if registry["password"] != None:
                oldPassword = input("Old password: ")
                oldPwHash = hashlib.md5(oldPassword.encode("utf-8")).hexdigest()

                if oldPwHash != registry["password"]:
                    call_error("Incorrect password.")
                    return

            newPassword = input("New password: ")
            newPwHash = hashlib.md5(newPassword.encode("utf-8")).hexdigest()
            registry["password"] = newPwHash

            with open(f"{sysdir}/reg.ldr", "w") as file:
                json.dump(registry, file)

            print("Updated successfully.")

        case "set":
            try:
                args[0]

            except IndexError:
                for i in registry:
                    print(f"{i}: {registry[i]}")

                return

            try:
                args[1]

            except:
                call_error("Not enough arguments. Use \"set x y\" with x being the variable and y being the value.")
                return

            key = args[0].strip()

            try:
                value = eval(args[1])

            except Exception as e:
                call_error(e)
                return

            registry[key] = value

            with open(f"{sysdir}/reg.ldr", "w") as file:
                json.dump(registry, file)

            print("Updated successfully.")

        case _:
            foundInPackages = False
            package = ""

            for path in pkg_paths:
                if command + ".py" in os.listdir(path):
                    foundInPackages = True
                    package = os.path.abspath(path + f"\\{command}.py")

            if foundInPackages:
                with open(package) as packageFile:
                    packageCode = packageFile.read()

                exec(packageCode, globals(), locals())

            else:
                call_error(f"Command not found: {command}")
