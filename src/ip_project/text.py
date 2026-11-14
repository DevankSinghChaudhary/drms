import time

from yaspin import yaspin

spinner = yaspin(text="Exiting the Application", color="cyan")
total_pass = 5
PASS = "FISH"

while total_pass > 0:
    print(f"Tries remaining: {total_pass}")
    while True:
        password = input("Enter Password: ")
        if password == "":
            print("Password cannot be empty")
            continue
        else:
            break

    if password == PASS:
        break
    else:
        set = total_pass = total_pass - 1
        if total_pass == 0:
            print("You are not authorized to access application")
            spinner.start()
            time.sleep(1)
            spinner.stop()

            break
        else:
            print("Wrong Password. Try Again")
            print()
