from newPostProcessing_LIB import *
import os, sys

# crea la cartella dei risultati, se non esiste già
try:
    os.makedirs(os.path.join(os.getcwd(), "results"))
except FileExistsError:
    sys.stdout.write("\nThe \'results\' folder already existed.\n")

#------------------------------------RESIDUI-------------------------------------------#
# salva i risultati in "Residui.png"


#------------------------------------COEFFICIENTI-------------------------------------------#
# coefficients(path, tick_spacing_x=, tick_spacing_y=)
# argomenti opzionali: tick_spacing_x e tick_spacing_y. definiscono lo spacing degli assi 
# del grafico. valori di default: x = 50, y = 0.05
# stampa i risultati in "Risultati analisi.txt" e salva i grafici in "Coefficienti.png"


#------------------------------------FORZE-------------------------------------------#
## IMPOSTAZIONI DA MODIFICARE ##

# scegliere se calcolare forze, momenti o entrambe le cose
force_calc = True # True, False, 1, 0
moment_calc = True # True, False, 1, 0

# modificano la spaziatura degli assi. default = 10
n_ticks_x = 10 
n_ticks_y = 10

#------------------------------------------------------------------------------------#

# ricerca automaticamente i nomi delle parti di cui si sono calcolate le forze nella simulazione
# in caso di errori, compilare a mano part_list e path_list
part_list = []
path_list = []

for root, dirs, files in os.walk(os.path.join(os.getcwd(), "postProcessing")):
    for i in range(len(dirs)):
        if re.search("[Ff]orces", dirs[i]):
            part_list.append(re.sub("[Ff]orces", "", dirs[i]))
    for file in files:
        if re.search("forces.dat", file):
            path_list.append(os.path.join(root, file))

        # trova il path del file con i residui e lancia residuals(path)
        if re.search("residuals.dat", file):
            residuals(os.path.join(root, file))

        # trova il path del file con i coefficienti e lancia coefficients(path)
        if re.search("forceCoeffs.dat", file):
            coefficients(os.path.join(root, file))


for path, part in zip(path_list, part_list):
    if re.search("global", part): part = re.sub("global", "Moto", part)
    forces(path, part, force_calc, moment_calc, n_ticks_x, n_ticks_y)