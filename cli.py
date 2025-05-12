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
print("2: start or reboot project")
print("3: update project")
print("4: remove project")
print("5: build project")
print("6: kill node")
if os.path.isfile("pl"):
    prCyan("pl: setup voor Polarlearn")

menu = input("wat wil je doen? \n")

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
    npm = input(
        "welke npm achtig software wil je gebruiken?\nnpm en pnpm zijn getest\n"
    )
    ngs.setup(projectnaam, repo_url, custom_branch, run_after_setup, npm)
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
elif menu == "pl":
    ngs.setup(
        "Polarlearn", "https://github.com/polarnl/PolarLearn", None, False, "pnpm"
    )
    os.chdir("Polarlearn")
    with open("prebuild.sh", "w") as f:
        f.write(
            """
            cd laatste_versie
            pnpx prisma db push
            cd ..
        """
        )
    with open("huidige_versie", "r") as f:
        versie = f.read().strip()
    os.chdir(versie)
    with open(".env", "w") as f:
        f.write(
            """
DATABASE_URL="mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019/polarlearn?replicaSet=rs0"
POLARLEARN_URL="http://localhost:3000"

AUTH_GOOGLE_ID="Stop hier de Google OAuth2 Client ID die je hebt gekregen van de google cloud console"
AUTH_GOOGLE_SECRET="Stop hier de Google OAuth2 Client Secret die je hebt gekregen van de google cloud console"
AUTH_GITHUB_ID="Stop hier de GitHub OAuth2 Client ID die je hebt gekregen van de GitHub Developer Settings"
AUTH_GITHUB_SECRET="Stop hier de GitHub OAuth2 Client Secret die je hebt gekregen van de GitHub Developer Settings"

AUTH_SECRET="qN6ix/Md3/429I4UcTe1fI61DtX/pQQWDv+fCoTT3lE="
AUTH_URL="http://localhost:3000"
SECRET="qN6ix/Md3/429I4UcTe1fI61DtX/pQQWDv+fCoTT3lE="
        """
        )
    os.chdir("..")
    os.chdir("..")
    ngs.build("Polarlearn")
