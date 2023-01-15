####################################################################
##       ____________     _____      ______      ___________      ##
##      |   ______  |    |     \    /     |     |   _______|      ##
##      |  |     |  |    |  |\  \  /  /|  |     |  |              ##
##      |  |_____|  |    |  | \  \/  / |  |     |  |_____         ##
##      |   ________|    |  |  \____/  |  |     |   _____|        ##
##      |  |             |  |          |  |     |  |              ##
##      |  |             |  |          |  |     |  |              ##
##      |__|             |__|          |__|     |__|              ##
##                                                                ##
####################################################################


# This script aims at the automation of the simulation running process.
# Ideally, one should be able to run this script, go to sleep, and wake up with all that's
# needed for the CFD post processing in ParaView.
# It starts by running the simulation, then the post processing (keeping track of the time
# needed to complete both), and then communicates the results to the Telegram Bot.

# Possible improvement points:
#   - create functions (e.g. for Telegram messages/Paraview, if included) to be imported from another .py file (more order);
#   - convert some cutting planes from vtk to png to be included in the pictures sent.

####################################################################

# TELEGRAM INFOS:

# CFD group ID: -1001568561105
# CFD channel ID: -1001580210471
# PMF_CFD_BOT API token: 2137946322:AAFTASN-baZ6iN_dN3e-l22r_WptXKLigNM
# prova channel ID: -1001775370943
####################################################################

###  COMMON TERMS TRANSLATIONS:  ###

##  'parafanghi'  =    mudguards  ##
##  'carena'      =    fairing    ##
##  'pilota'      =    rider      ##
##  'alette'      =    wings      ##
##  'coda'        =    tail       ##


####################################################################

# setting up telegram
tg = True
if tg:
    import telegram
    bot = telegram.Bot(token='2137946322:AAFTASN-baZ6iN_dN3e-l22r_WptXKLigNM')
    chat_id = ["-1001580210471"]

def tg_message(tg, text):
    if tg:
        global bot, chat_id

        for id in chat_id:
            bot.sendMessage(id, text)


# importing all the necessary modules
import itertools, os, re, sys, threading, time, subprocess, pathlib


# flexing loretet's ASCII drawing's skills
print('''
__________________________________________________

         ______________    _____________
         \________     \  /     _______/
            ______|  |\ \/ /|  |______
            \_____   | \  / |   _____/
                  |  |  \/  |  |
                   \ |      | /
                    \|      |/

__________________________________________________

''')
time.sleep(0.3)

# initiating variables
cwd = os.getcwd()
cwd = pathlib.Path(cwd)
good = True

# log in
while True:
    name = str(input("Who are you? ")).title()
    name = name.strip()
    if not (name.isalpha()):
        print("Please, insert your name without any numbers or punctuation marks.\n")
        continue

    sys.stdout.write(f"Hello {name} :) \n")
    time.sleep(0.3)
    break

# creation of the 0/ and system/ directories, if needed
while True:
    try:
        dir = input("\nDo you need to create the 0/ and system/ directories? (y/n): ").lower()
    except: 
        print("\nPlease only insert y or n as an answer")
        continue

    if dir == "y":
        try:
            exec(open("./directories.py").read())
        except Exception as Er:
            print(f"\nSomething went wrong during the creation of the directories. Error: {Er}")
            good = False
        break
    elif dir == "n":
        break
    

while True and good:
    try:
        dir = input("\nDo you want to start the simulation? (y/n): ").lower()
    except: 
        print("\nPlease only insert y or n as an answer")
        continue

    if dir == "y":
        break
    elif dir == "n":
        good = False
        break


if good:
    while True:
        try:
            eta = float(input("ETA of the simulation (hours.minutes): "))
            break
        except:
            print("Only numbers and points allowed. Use . as separator, if needed.\n")

    while True:
        desc = input("Write a short description of your simulation (case, pc...): ")
        if desc.isprintable(): 
            break
        else:
            print("Only printable characters allowed.\n")

    # Telegram bot announces that somebody started a simulation
    tg_message(tg, f"{name} just started a simulation ({desc}). ETA: {eta} hours.")

if good:       
    # shell running 'sh Allrun.sh' to run the simulation
    time.sleep(0.1)
    start_sim = time.time()
    sys.stdout.write("\nStarting the simulation...\n")

    # loading animation (why needed? Because yes.)
    done = False
    def animate():
        for char in itertools.cycle( ['|','/','-','\\'] ):
            if done:
                break
            sys.stdout.write('\r' + char)
            sys.stdout.flush()
            time.sleep(0.2)
        sys.stdout.write(" ")

    threading.Thread(target=animate).start()

    # running the Allrun
    try:
        subprocess.run(["sh", "Allrun.sh"], check=True)
    except Exception as Er:
        print(f"\nSomething went wrong during the simulation. Error: {Er}")
        tg_message(tg, f"{name}'s simulation crashed for some reason. Error: {Er}")
        good = False
    done = True

# printing of simulation time on console and on Telegram
pp = True
if good:
    end_sim = time.time()
    sim_time = end_sim - start_sim
    sim_time_hour = sim_time/ 60 / 60

    if sim_time_hour > 1:
        sim_time_hour = int(sim_time_hour)
        sim_time_min = int((sim_time-(sim_time_hour*60*60))/60)
        sys.stdout.write(f"\nThe simulation has ended and lasted {sim_time_hour}:{sim_time_min} hours.\n")
        tg_message(tg, f"{name}'s simulation ended after {sim_time_hour} hours.")
    else:
        sim_time_min = round(sim_time/60, 2)
        sys.stdout.write(f"\nThe simulation has ended and lasted {sim_time_min} minutes.\n")
        tg_message(tg, f"{name}'s simulation ended after {sim_time_min} minutes.")

    # starts post processing
    sys.stdout.write("\nStarting post processing automation...")
    time.sleep(0.6)
    start_pp = time.time()

    try: 
        exec(open("./newPostProcessing.py").read())
        
        # prints the time used for post processing
        end_pp = time.time()
        pp_time_min = round(( ( end_pp-start_pp ) / 60 ), 2 )
        time.sleep(0.8)
        sys.stdout.write("The post processing has ended and lasted " + str( pp_time_min ) + " minutes." + '\n')
        tg_message(tg, f"{name}'s simulation ({desc}) has been post processed in {pp_time_min} minutes.")


    except Exception as Er:
        print(f"Something went wrong during post processing. Error:\n{Er}")

        tg_message(tg, f"{name}'s simulation couldn't be post processed for some reason. Last error:\n{Er}")
        pp = False


####################################################################


# sends the pictures in the 'results' folder
if tg and pp and good:

    sys.stdout.write("\nSending results ...\n")

    done = False
    threading.Thread(target=animate).start()

    # crea la lista di immagini da inviare e la lambda function per tagliarla (send_media_group permette di inviare solo 10 immagini per volta)
    images = []
    final_list = lambda start_list: [start_list[i:i+10] for i in range(0, len(start_list), 10)]

    for root, dirs, files in os.walk(cwd / "results"):
        root = pathlib.Path(root)
        for f in files:
            if re.search("\.txt$", f):
                txt = root / f
                continue
            images.append(telegram.InputMediaPhoto(open(root / f, 'rb')))
    
    images_final = final_list(images)
        
    try:
        for id in chat_id:
            bot.send_document(id, open(txt))
        for chunk in images_final:
            bot.send_media_group(id, chunk)
    except Exception as Er:
        print(f"Something went wrong during the sending of the documents. Error:\n{Er}")
    done = True

if good:
    sys.stdout.write("Everything's done! Quitting...\n")
    time.sleep(1)
else:
    print("\nQuitting ...\n")
    time.sleep(1)