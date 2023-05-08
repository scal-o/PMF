# code by scalo

import os, sys, pathlib
sys.path.append(os.getcwd())
from newPostProcessing_LIB import *


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

# creates a dictionary for parts and paths
parts_paths = {}
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if re.search(".dat$", file):
            part_name = re.search("(force_?[a-zA-Z_]+|globalForces|residuals|wallTau|y\+)", root).group()   # finds the part name from the file path
            if re.search("[fF]orces", part_name):                                                           # assigns the final part name
                part_name = re.sub("[fF]orces", "", part_name)
            if re.search("global", part_name):
                part_name = re.sub("global", "Moto", part_name)
            parts_paths.setdefault(part_name, [])                                                           
            parts_paths[part_name].append(pathlib.Path(os.path.join(root, file)))                           # creates a dictionary with the part_name : part_path pair

print(parts_paths)

for key in parts_paths.keys():
    if len(parts_paths[key]) > 1:

        new_paths = []

        for path in parts_paths[key]:                                                                       # moves the old .dat files in new directories
            new_path = pathlib.Path(str(path.parent) + "_old")
            if not new_path.is_dir(): new_path.mkdir()
            new_path = new_path / path.name

            path.replace(new_path)
            if re.search("[1-9][0-9]+$", str(path.parent)): path.parent.rmdir()                             # leaves the original 0 directory
            else: new_paths.append(path)

            new_paths.append(new_path)
        parts_paths.update({key : new_paths})                                                               # updates the paths in the dictionary

        parts_paths[key].sort()                                                                                 # sorts the paths

        with parts_paths[key][1].open() as pipefile_start, parts_paths[key][2].open() as pipefile_end, parts_paths[key][0].open("w") as endfile:

            end_lines = pipefile_end.readlines()
            for line in end_lines:
                if re.search("^([1-9][0-9]+)", line):                                                           # looks for the first line with actual values
                    new_iterations_t = re.search("^([1-9][0-9]+)", line).group()
                    new_iterations_index = end_lines.index(line) if not re.search("residuals", endfile.name) else end_lines.index(line) +1
                    break

            start_lines = pipefile_start.readlines()
            for line in start_lines:                                                                            # looks for the last compatible line
                if re.search(f"^{new_iterations_t}", line):
                    old_iterations_last_index = start_lines.index(line) if not re.search("residuals", endfile.name) else start_lines.index(line) -1
                    break
                    
            new_lines = start_lines[:old_iterations_last_index] + end_lines[new_iterations_index:]
            endfile.writelines(new_lines)                                                                       # writes the new lines in the correct file


for part in parts_paths.keys():
    path = parts_paths[part][0]

    if re.search("Moto", part): 
        forces(path, part, force_calc, moment_calc, n_ticks_x, n_ticks_y)
        part = re.sub("Moto", "Moto con porosità", part)
        
    # trova il path del file con i residui e lancia residuals(path)
    elif re.search("residuals.dat", str(path)):
        residuals(path)
        continue

    # trova il path del file con i coefficienti e lancia coefficients(path)
    elif re.search("forceCoeffs.dat", str(path)):
        coefficients(path)
        continue

    elif re.search("y\+|wallTau", str(path)):
        continue
    
    forces(path, part, force_calc, moment_calc, n_ticks_x, n_ticks_y)