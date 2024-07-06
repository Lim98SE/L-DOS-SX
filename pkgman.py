#!/bin/python3
def main(args):
    url = "https://www.lim95.com/pkgman"
    try:
        args[0]

    except:
        call_error("No arguments.")
        return

    if args[0].lower().strip() == "search":
        try:
            args[1]

        except:
            call_error("No query.")
            return
        
        response = requests.post(f"{url}/query", json={"query": args[1]})
        responseJson = response.json()

        for i in responseJson:
            print(i)

    if args[0].lower().strip() == "install":
        try:
            args[1]

        except:
            call_error("No package provided.")
            return

        try:
            response = requests.post(f"{url}/get", json={"name": args[1]})

        except Exception as e:
            call_error(f"An error occured: {e}")

        try:
            responseJson = response.json()

        except:
            print(response.content)
            

        if "error" in responseJson.keys():
            call_error(responseJson["error"])
            return

        if "package" in responseJson.keys():
            with open(f"{sysdir}\\packages\\{responseJson['name']}.py", "w") as pkgfile:
                pkgfile.write(responseJson["package"])

        if registry["useColor"]:
            print(f"{colorama.Fore.GREEN}Installed {responseJson['name']} successfully.{colorama.Style.RESET_ALL}")

        else:
            print(f"Installed {responseJson['name']} successfully.")

    if args[0].lower().strip() == "remove":
        try:
            args[1]

        except:
            call_error("No package provided.")
            return

        for i in pkg_paths:
            if args[1].strip() + ".py" in os.listdir(i):
                os.remove(f"{i}/{args[1].strip() + '.py'}")
                if registry["useColor"]:
                    print(f"{colorama.Fore.GREEN}Removed {args[1].strip()} successfully.{colorama.Style.RESET_ALL}")

                else:
                    print(f"Removed {args[1].strip()} successfully.")

                return

        call_error(f"{args[1].strip()} not found.")

main(args)
