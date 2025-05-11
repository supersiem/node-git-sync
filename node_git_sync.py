import os
import colorprint
import subprocess


if __name__ == "__main__":
    colorprint.prRed("deze file kan niet worden uitgevoerd, gebruik cli.py")


def ternimal_met_output(command):
    try:
        output = subprocess.check_output(command, text=True).strip()
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def start(projectnaam):
    os.chdir(projectnaam)
    with open(f"{projectnaam}_huidige_versie.txt", "r") as f:
        huidige_versie = f.read().strip()
    os.chdir(huidige_versie)
    colorprint.prGreen(f"het project {projectnaam} word gestart")
    colorprint.prYellow("de oude server wordt gestopt")
    os.system('pkill -f "node"')
    colorprint.prYellow("de nieuwe server wordt gestart")
    os.system("nohup pnpm start &")
    colorprint.prGreen("Klaar!")


def setup(projectnaam, repo_url, custom_branch, run_after_setupA):
    run_after_setup = run_after_setupA
    skip_build = False
    if os.path.exists(projectnaam):
        print("project bestaat al")
        return
    os.mkdir(projectnaam)
    os.chdir(projectnaam)
    os.system(f"git clone {repo_url}")
    os.chdir(projectnaam)
    huidige_versie = ternimal_met_output(["git", "rev-parse", "--short", "HEAD"])
    if custom_branch:
        os.system(f"git checkout {custom_branch}")

    colorprint.prYellow("de dependencies worden geinstalleerd")
    build_result = subprocess.run(["pnpm", "install"], text=True)
    if build_result.returncode != 0:
        colorprint.prRed("het installen van de modules is mislukt!")
        if run_after_setupA:
            colorprint.prRed("het project kan daarom straks niet worden gestart!")
        run_after_setup = False
        skip_build = True

    if not skip_build:
        colorprint.prYellow("het project worden gebuild")
        build_result = subprocess.run(["pnpm", "build"], capture_output=True)
        if build_result.returncode != 0:
            colorprint.prRed("de build is mislukt!")
            run_after_setup = False
            if run_after_setupA:
                colorprint.prRed("het project kan daarom straks niet worden gestart!")

    os.chdir("..")
    with open(f"{projectnaam}_huidige_versie.txt", "x") as f:
        f.write(huidige_versie)
    os.rename(projectnaam, huidige_versie)
    print("setup klaar!")
    colorprint.prGreen(
        "voeg code die je wilt laten uitvoeren bij een update voor de build toe aan het bestand prebuild.sh"
    )
    with open(f"prebuild.sh", "x") as f:
        f.write("#!/bin/bash\n")

    if run_after_setup:
        start(projectnaam)


def update(projectnaam):
    os.chdir(projectnaam)
    with open(f"{projectnaam}_huidige_versie.txt", "r") as f:
        huidige_versie = f.read().strip()
    os.chdir(huidige_versie)
    os.system("git fetch")
    local_head = ternimal_met_output(["git", "rev-parse", "HEAD"])
    remote_head = ternimal_met_output(["git", "rev-parse", "@{u}"])
    if local_head == remote_head:
        colorprint.prRed("er is GEEN update beschikbaar")
    else:
        colorprint.prGreen("er is een update beschikbaar")
        colorprint.prYellow(
            "er word een kopie gemaakt voor de laatse versie dit kan even duren...."
        )
        os.chdir("..")

        os.makedirs("laatste_versie")
        os.system(
            f"rsync -av --exclude='node_modules' {huidige_versie}/ laatste_versie/"
        )
        os.chdir("laatste_versie")
        colorprint.prYellow("de update word opgehaalt")
        os.system("git pull")
        colorprint.prYellow("de dependencies worden geupdate")
        os.system("pnpm install")
        colorprint.prYellow("het prebuild script word uitgevoerd")
        os.chdir("..")
        os.system("bash prebuild.sh")
        os.chdir("laatste_versie")
        colorprint.prYellow("de update word gebuild")
        build_result = subprocess.run(["pnpm", "build"], text=True)
        if build_result.returncode != 0:
            colorprint.prRed("de build is mislukt!")
            colorprint.prRed("de laatste versie word verwijderd")
            os.chdir("..")
            os.system("rm -rf laatste_versie")
            colorprint.prRed("Update mislukt door dat de build mislukt is")
            return

        colorprint.prYellow("het bestand met de laatste versie word geupdate")
        laatste_versie = ternimal_met_output(["git", "rev-parse", "--short", "HEAD"])
        os.chdir("..")
        os.rename("laatste_versie", laatste_versie)
        colorprint.prYellow("de folder met de laatste versie word hernoemd")
        with open(f"{projectnaam}_huidige_versie.txt", "w") as f:
            f.write(laatste_versie)
        colorprint.prYellow("de versie word geupdate")
        os.chdir("..")
        start(projectnaam)
        os.chdir("..")
        colorprint.prYellow("de folder met de oude versie word verwijderd")
        os.system(f"rm -rf {huidige_versie}")
        colorprint.prGreen("update klaar!")


def build(projectnaam):
    os.chdir(projectnaam)
    os.system("bash prebuild.sh")
    with open(f"{projectnaam}_huidige_versie.txt", "r") as f:
        huidige_versie = f.read().strip()
    os.chdir(huidige_versie)
    os.system("pnpm build")
    colorprint.prGreen("build klaar!")
