#!/bin/python3
def main(args):
    def update_cmdint():
        import requests
        import hashlib
        server = "https://www.lim95.com"

        print("Checking with server...")

        try:
            req = requests.get(f"{server}/static/ldsx/cmdint.py")

        except requests.exceptions.ConnectionError:
            call_error("Can't connect to the server.")
            return

        with open(f"{sysdir}//cmdint.py", "rb") as file:
            cmdint_current = hashlib.md5(file.read()).hexdigest()

        new_hash = hashlib.md5(req.content).hexdigest()

        if new_hash == cmdint_current:
            call_error("No updates for cmdint are available.")
            return

        with open(f"{sysdir}//cmdint.py", "wb") as file:
            file.write(req.content)

        return True

    def update_main():
        import requests
        import hashlib
        server = "https://www.lim95.com"

        print("Checking with server...")

        try:
            req = requests.get(f"{server}/static/ldsx/main.py")

        except requests.exceptions.ConnectionError:
            call_error("Can't connect to the server.")
            return

        with open(f"{home}//main.py", "rb") as file:
            current = hashlib.md5(file.read()).hexdigest()

        new_hash = hashlib.md5(req.content).hexdigest()

        if new_hash == current:
            call_error("No updates for main are available.")
            return

        with open(f"{home}//main.py", "wb") as file:
            file.write(req.content)

        return True
    
    a = update_cmdint()
    b = update_main()

    if a or b:
        print("Updated successfully! Reloading...")
        
        with open(f"{sysdir}//..//main.py", "r") as file:
            cmdint = file.read()

        exec(cmdint)
    
    return

main(args)
