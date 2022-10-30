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
#   - include some Paraview automated post processing for streamlines;
#   - create functions (e.g. for Telegram messages/Paraview, if included) to be imported from another .py file (more order);
#   - convert some cutting planes from vtk to png to be included in the pictures sent.

####################################################################


# TELEGRAM INFOS:

# CFD group ID: -1001568561105
# CFD channel ID: -1001580210471
# @loretet's chat ID: 693374266
# PMF_CFD_BOT API token: 2137946322:AAFTASN-baZ6iN_dN3e-l22r_WptXKLigNM
#"Tre dell'ave maria" channel ID: -1001172054206

####################################################################


# flags to decide whether to use Telegram
tg = True

# importing all the necessary modules

import itertools, os, math, re, sys, threading, time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
if tg:
    import telegram, telegram_send

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

# initialization of some useful variables
file = __file__
perc = os.path.dirname(file)
cwd = os.getcwd()
if tg:
    bot = telegram.Bot(token='2137946322:AAFTASN-baZ6iN_dN3e-l22r_WptXKLigNM')
    chat_id = ["-1001580210471"]

# log in
while True:
    name = str(input("Who are you? ")).title()
    lista_name = list(name)
    for i in lista_name:
        if i.isspace():
            lista_name.remove(i)
    name_join = "".join(lista_name)
    if not (name_join.isalpha()):
        print("Please, insert your name without any numbers or punctuation marks.\n")
        continue
    break

while True:
    try:
        eta = float(input("ETA of the simulation (hours.minutes): "))
        break
    except:
        print("Only numbers and points allowed. Use . as separator, if needed.\n")

sys.stdout.write(f"Hello {name} :) \n")
time.sleep(0.3)


# creation of the 'results' folder to store the post processing results
try:
    os.makedirs(os.path.join(perc, "results"))
except FileExistsError:
    sys.stdout.write("\nThe \'results\' folder already existed.\n")

# Telegram bot advises that somebody started a simulation
if tg:
    for id in chat_id:
        bot.sendMessage(id, f"{name} just started a simulation. ETA: {eta} hours.")

# shell running 'sh Allrun.sh' to run the simulation
time.sleep(0.4)
start_sim = time.time()
os.system("echo ")
os.system("echo Starting the simulation...")

# loading animation (why needed? Because yes.)
done = False
os.system("echo ")
def animate():
    for char in itertools.cycle( ['|','/','-','\\'] ):
        if done:
            break
        sys.stdout.write('\r' + char)
        sys.stdout.flush()
        time.sleep(0.2)
    os.system("echo ")

threading.Thread(target=animate).start()

# running the Allrun
good = True
try:
    os.system("sh Allrun.sh")
    done = True
except:
    good = False

# printing of simulation time on console and on Telegram
if good:
    end_sim = time.time()
    sim_time_min = round(( (end_sim-start_sim ) / 60) , 2)
    sim_time_hour = round(( ( ( end_sim-start_sim ) / 60 ) / 60 ), 2)
    if sim_time_hour > 1:
        sys.stdout.write("\nThe simulation has ended and lasted " + str( sim_time_hour ) + " hours." + '\n')
        if tg:
            for id in chat_id:
                bot.sendMessage(id, f"{name}'s simulation ended after {sim_time_hour} hours.")
    else:
        sys.stdout.write("\nThe simulation has ended and lasted " + str( sim_time_min ) + " minutes." + '\n')
        if tg:
            for id in chat_id:
                bot.sendMessage(id, f"{name}'s simulation ended after {sim_time_min} minutes.")

    # inizio il post processing
    os.system("echo '\nStarting post processing automation...'")
    time.sleep(0.6)
    start_pp = time.time()


####################################################################


###  COMMON TERMS TRANSLATIONS:  ###

##  'parafanghi'  =    mudguards  ##
##  'carena'      =    fairing    ##
##  'pilota'      =    rider      ##
##  'alette'      =    wings      ##
##  'coda'        =    tail       ##


####################################################################

if good: 
    try: 
        exec(open("./newPostProcessing.py").read())
        
        # prints the time used for post processing
        end_pp = time.time()
        pp_time_min = round(( ( end_pp-start_pp ) / 60 ), 2 )
        time.sleep(0.8)
        sys.stdout.write("The post processing has ended and lasted " + str( pp_time_min ) + " minutes." + '\n')
        if tg:
            for id in chat_id:
                bot.sendMessage(id, f"{name}'s simulation has been post processed in {pp_time_min} minutes.")
        pv = True

    except Exception as er:
        print("Something went wrong during post processing. Error:\n")
        print(er)
        # pv = False
        if tg:
            for id in chat_id:
                bot.sendMessage(id, f"{name}'s simulation couldn't be post processed for some reason. Last error:\n {er}")


####################################################################


# ends the script
if good:
    os.system("echo ")
    time.sleep(0.6)
    if pv:
        sys.stdout.write("The case is ready to be studied in Paraview." + '\n' + "Remember to have a look inside the \'results\' folder!\n")
    else:
        sys.stdout.write("The case is ready to be studied in Paraview!\n")
else:
    print("Something went wrong during the simulation.")
    if tg:
        for id in chat_id:
            bot.sendMessage(id, f"{name}'s simulation crashed for some reason.")


####################################################################


# sends the pictures in the 'results' folder
if tg and pv:

    # crea la lista di immagini da inviare e la lambda function per tagliarla (send_media_group permette di inviare solo 10 immagini per volta)
    images = []
    final_list = lambda start_list: [start_list[i:i+10] for i in range(0, len(start_list), 10)]

    for root, dirs, files in os.walk(os.path.join(cwd, "results")):
        for f in files:
            if re.search("\.txt$", f):
                txt = os.path.join(root, f)
                continue
            images.append(telegram.InputMediaPhoto(open(os.path.join(root,f), 'rb')))
    
    images_final = final_list(images)
        
    for id in chat_id:
        bot.send_document(id, open(txt))
        for chunk in images_final:
            bot.send_media_group(id, chunk)