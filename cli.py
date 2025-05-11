import node_git_sync as ngs
import os
from colorprint import *

os.system("clear")
# gemakt met https://patorjk.com/software/taag/#p=display&f=Big%20Money-ne&t=node%20git%20sync
print(
    """
                           /$$                           /$$   /$$                                                  
                          | $$                          |__/  | $$                                                  
 /$$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$         /$$$$$$  /$$ /$$$$$$          /$$$$$$$ /$$   /$$ /$$$$$$$   /$$$$$$$
| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$       /$$__  $$| $$|_  $$_/         /$$_____/| $$  | $$| $$__  $$ /$$_____/
| $$  \ $$| $$  \ $$| $$  | $$| $$$$$$$$      | $$  \ $$| $$  | $$          |  $$$$$$ | $$  | $$| $$  \ $$| $$      
| $$  | $$| $$  | $$| $$  | $$| $$_____/      | $$  | $$| $$  | $$ /$$       \____  $$| $$  | $$| $$  | $$| $$      
| $$  | $$|  $$$$$$/|  $$$$$$$|  $$$$$$$      |  $$$$$$$| $$  |  $$$$/       /$$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$
|__/  |__/ \______/  \_______/ \_______/       \____  $$|__/   \___/        |_______/  \____  $$|__/  |__/ \_______/
                                               /$$  \ $$                               /$$  | $$                    
                                              |  $$$$$$/                              |  $$$$$$/                    
                                               \______/                                \______/                     
"""
)
prCyan("welkom bij node_git_sync")
print("dit kan je doen:")
print("1: setup project")
print("2: start project")
print("3: update project")
print("4: remove project")
print("5: build project")
print("6: kill node")

menu = input("wat wil je doen? \n")

print("\n")
if menu == "1":
    projectnaam = input("wat is de naam van het project? \n")
    repo_url = input("wat is de url van het project? \n")
    custom_branch_tf = input(
        "will je een aangepaste branch of versie gebruiken? (y/N) \n"
    )

    if custom_branch_tf.lower() == "y" or custom_branch_tf.lower() == "yes":
        custom_branch = input("wat is de naam van de aangepaste branch? \n")
    else:
        custom_branch = None

    build_tf = input("will je het project starten na de setup? (Y/n) \n")
    if build_tf.lower() == "n" or build_tf.lower() == "nee" or build_tf.lower() == "no":
        run_after_setup = False
    else:
        run_after_setup = True

    ngs.setup(projectnaam, repo_url, custom_branch, run_after_setup)
    prGreen("het project is aangemaakt!")
elif menu == "2":
    ngs.start(input("wat is de naam van het project? \n"))
elif menu == "3":
    ngs.update(input("wat is de naam van het project? \n"))
elif menu == "4":
    os.system(f"rm -rf {input('wat is de naam van het project? \n')}")
    prGreen("Klaar!")
elif menu == "5":
    ngs.build(input("wat is de naam van het project? \n"))
elif menu == "6":
    os.system("pkill -f 'pnpm'")
