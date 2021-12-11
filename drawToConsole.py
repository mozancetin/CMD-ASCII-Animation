import drawASCIIart
import cv2
import os
from time import sleep
import json
import PIL.Image

def getImages(file : str, customFPS : int = -1):
    filtered = file.replace('\\', '/').split('/')[-1].split('.')[0].lower()
    if not os.path.exists("./pics/" + filtered):
        os.mkdir("./pics/" + filtered)

    path = "./pics/" + filtered + "/"
    vidcap = cv2.VideoCapture(file)
    FPS = vidcap.get(cv2.CAP_PROP_FPS)
    success,image = vidcap.read()
    count = 0
    while success:
        if customFPS != -1:
            if count % customFPS == 0:
                cv2.imwrite(path + "frame%d.jpg" % count, image) 
        else:
            cv2.imwrite(path + "frame%d.jpg" % count, image)

        success, image = vidcap.read()            
        count += 1
    
    data = dict()
    data["FPS"] = int(FPS)
    data["Width"] = float((PIL.Image.open(f"./pics/{filtered}/frame0.jpg")).size[0])

    with open(path + "data.json", "w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=True, indent=4)
    return FPS

def startAnimation(folder : str):
    print("Animation starting in 2 sec...")
    sleep(2)
    images = os.listdir(f"./pics/{folder}")
    data = json.load(open(f"./pics/{folder}/data.json", "r", encoding="utf-8-sig"))
    FPS = data["FPS"]
    imageSize = data["Width"]
    mul = imageSize * 2.3 / 960
    for i in range(0, len(images)):
        if f"frame{i}.jpg" in images:
            terminalsize = os.get_terminal_size()
            drawASCIIart.path = os.getcwd() + f"\\pics\\{folder}\\frame{i}.jpg"
            drawASCIIart.main(drawASCIIart.setSize(int(terminalsize.lines * mul)), drawASCIIart.setWidth(float(1)))
            sleep(1 / FPS)

def fileManager():
    folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    while(True):
        os.system('cls')
        count = 1
        things = list()
        print("Current folder: " + folder + "\n")
        for i in os.listdir(folder):
            if i.endswith(".mp4") or os.path.isdir(folder + f"/{i}"):
                print(f"[ {count} ] - {i}")
                things.append(i)
                count += 1
        
        print("\n[ -1 ] - Cancel")
        print("[ -2 ] - .. ( Upper folder )")

        try:
            choice = int(input("\nSelect a directory for enter in it or select an mp4 file for extracting it: "))
        except Exception:
            print("\nSelect a NUMBER from the list.")
            input("Press enter to continue...")
            os.system('cls')
            continue

        if choice == -1:
            break

        if choice == -2:
            paths = folder.split("\\")
            if len(paths) > 1:
                folder = "\\".join([path for path in paths if path != paths[-1]])
                if len(folder) == 2:
                    folder = folder + "\\"
            else:
                print("You can't go upper folder from here.")
                input("Press enter to continue...")
            os.system('cls')
            continue

        if choice <= 0 or choice >= count:
            print("\nInvalid operation\n")
            input("Press enter to continue...")

        else:
            thing = things[choice - 1]
            print(f"\n\nYour choice: {thing}")
            if str(thing).endswith(".mp4"):
                sure = input("\nDo you really want to extract it [Y/n]: ")
                if sure.lower().strip() == "" or sure.lower().strip() == "y":
                    print("Extraction started please wait...")
                    getImages(folder + "\\" + thing)
                    print("File extracted.")
                    sure2 = input("\nDo you really want to play it now [Y/n]: ")
                    if sure2.lower().strip() == "" or sure2.lower().strip() == "y":
                        os.system('cls')
                        startAnimation(thing.split(".")[0])
                        print("\n\nAnimation Ended.")
                        input("Press enter to continue...")
                    return
                elif sure.lower().strip() == "n":
                    continue
            else:
                folder = os.path.join(folder, thing)

def menu():
    if not os.path.exists("./pics/"):
        os.mkdir("./pics/")

    while(True):
        os.system('cls')
        print("""Select:
        
    [ 1 ] - Select Video To Extract Images
    [ 2 ] - Start Animation From Extracted
    [ 3 ] - Delete Extracted Animations
    
    [ 9 ] - Quit

        """)
        try:
            action = int(input("Waiting for input: "))
        except Exception:
            print("Invalid operation.")
            continue

        if action == 1:
            fileManager()
            
        elif action == 2:
            os.system('cls')
            foldernames = os.listdir("./pics")
            folderindex = 1
            folders = list()
            print("Exracted Animations:\n")
            while(True):
                for folder in foldernames:
                    if os.path.isdir(f"./pics/{folder}"):
                        print(f"[ {folderindex} ] - {folder}")
                        folders.append(folder)
                        folderindex += 1
                print("\n[ -1 ] - Cancel")
                try:
                    selectFolder = int(input("\nSelect Animation: "))
                    break
                except Exception:
                    folderindex = 1
                    print("\nSelect a NUMBER from the list.")
                    input("Press enter to continue...")
                    os.system('cls')

            if selectFolder == -1:
                folderindex = 1
                continue

            if selectFolder <= 0 or selectFolder >= folderindex:
                print("\nInvalid operation\n")
                input("Press enter to continue...")
            else:
                print(f"\n\nYour choice: {folders[selectFolder - 1]}")
                sure = input("\nDo you really want to start animation [Y/n]: ")
                if sure.lower().strip() == "" or sure.lower().strip() == "y":
                    os.system('cls')
                    startAnimation(folders[selectFolder - 1])
                    print("\n\nAnimation Ended.")
                    input("Press enter to continue...")
                elif sure.lower().strip() == "n":
                    continue
            
            folderindex = 1

        elif action == 3:
            os.system('cls')
            foldernames = os.listdir("./pics")
            folderindex = 1
            folders = list()
            print("Exracted Animations:\n")
            while(True):
                for folder in foldernames:
                    if os.path.isdir(f"./pics/{folder}"):
                        print(f"[ {folderindex} ] - {folder}")
                        folders.append(folder)
                        folderindex += 1
                print("\n[ -1 ] - Cancel")
                try:
                    selectFolder = int(input("\nSelect Animation: "))
                    break
                except Exception:
                    folderindex = 1
                    print("\nSelect a NUMBER from the list.")
                    input("Press enter to continue...")
                    os.system('cls')

            if selectFolder == -1:
                folderindex = 1
                continue

            if selectFolder <= 0 or selectFolder >= folderindex:
                print("\nInvalid operation\n")
                input("Press enter to continue...")
            else:
                print(f"\n\nYour choice: {folders[selectFolder - 1]}")
                sure = input("\nDo you really want to start animation [Y/n]: ")
                if sure.lower().strip() == "" or sure.lower().strip() == "y":
                    for file in os.listdir(f"./pics/{folders[selectFolder - 1]}"):
                        os.remove(f"./pics/{folders[selectFolder - 1]}/{file}")
                    os.rmdir(f"./pics/{folders[selectFolder - 1]}")
                elif sure.lower().strip() == "n":
                    continue
            
            folderindex = 1

        elif action == 9:
            break

menu()