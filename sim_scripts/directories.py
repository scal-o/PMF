import os, re, warnings
from shutil import copy
import pathlib

def sub(regex, new_line, skipline=False):
    global line, new_lines, f
    while not re.search("\}", line):
        if re.search(regex, line):
            new_lines.append(new_line)
            if skipline: 
                line = f.readline()
        else: new_lines.append(line)
        line = f.readline() 

def enlist_patches(to_remove):
    global line, new_lines, c, carena, paraf_ant, paraf_post, patches_list
    patches_list = []
    while not re.search("\)", line):
        if re.search("\(", line):
            new_lines.append(line)
        elif not re.search(to_remove, line):
            patches_list.append(line)
        line = c.readline() 
    patches_list.sort()

    global pilota
    pilota = False
    casco = False
    carena = False
    paraf_ant = False
    paraf_post = False
    alette = False
    muro = False

    for patch in patches_list:
        new_lines.append(patch)

        if re.search("carena", patch):
            if carena == False:
                carena = []
            carena.append(patch.strip("\t\n"))
        elif re.search("parafango_ant", patch):
            if paraf_ant == False:
                paraf_ant = []
            paraf_ant.append(patch.strip("\t\n"))
        elif re.search("parafango_post", patch):
            if paraf_post == False:
                paraf_post = []
            paraf_post.append(patch.strip("\t\n"))

        elif re.search("wing", patch):
            if alette == False:
                alette = []
            alette.append(patch.strip("\t\n"))
        elif re.search("muro", patch):
            muro = True

        elif re.search("pilota", patch):
            if not pilota:
                pilota = []
            pilota.append(patch.strip("\t\n"))
        elif re.search("casco", patch):
            casco = True

    if not (pilota and casco):
        warnings.warn("Patches \"pilota\" and \"casco\" not found")
    elif not carena:
        warnings.warn("Patch containing \"carena\" not found")
    elif not paraf_ant:
        warnings.warn("Patch containing \"parafango_ant\" not found")
    elif not paraf_post:
        warnings.warn("Patch containing \"parafango_post\" not found")

def check_am():
    alette = False
    muro = False
    flap = False
    global line, new_lines, c

    while not re.search("\)", line):
        if re.search("wing", line):
            if not alette:
                alette = []
            alette.append(line.strip("\t\n"))
            if re.search("flap", line):
                flap = line.strip("\t\n")
        elif re.search("muro", line):
            muro = True
        line = c.readline()

    return alette, muro, flap    

print("\nScript to create 0/ and system/ dirs")

default = ""
flag = False

while default == "" or flag == False:

    try:
        default = input("\nShould default data for speed be used? (y/n): ").lower()
    except: 
        print("\nPlease only insert y or n as an answer")

    if default == "y":
        speed = "-50"
        flag = True

    elif default == "n":
        while True:
            speed = input("\nSpeed (default -50): ")
            try:
                int(speed)
                break
            except:
                print("\nInvalid input. Correct format: int")
        
        flag = True
    else: print("\nPlease only insert y or n as an answer")


cwd = os.getcwd()
cwd = pathlib.Path(cwd)


general_fun_dir = pathlib.Path("/mnt/p/script/system")
if not general_fun_dir.is_dir():
    general_fun_dir = pathlib.Path("C:/Users/alexs/Documents/GitHub/PMF/general_functions")
if not general_fun_dir.is_dir():
    general_fun_dir = pathlib.Path("/mnt/c/users/alexs/Documents/GitHub/PMF/general_functions")

wall_functions_dir = pathlib.Path("/mnt/p/script/system/wall_functions")
if not wall_functions_dir.is_dir():
    wall_functions_dir = pathlib.Path("C:/Users/alexs/Documents/GitHub/PMF/wall_functions")
if not wall_functions_dir.is_dir():
    wall_functions_dir = pathlib.Path("/mnt/c/users/alexs/Documents/GitHub/PMF/wall_functions")

wing_functions_dir = pathlib.Path("/mnt/p/script/system/wing_functions")
if not wing_functions_dir.is_dir():
    wing_functions_dir = pathlib.Path("C:/Users/alexs/Documents/GitHub/PMF/wing_functions")
if not wing_functions_dir.is_dir():
    wing_functions_dir = pathlib.Path("/mnt/c/users/alexs/Documents/GitHub/PMF/wing_functions")

zero_dir = cwd / "0"
system_dir = cwd / "system"


for file in os.scandir(zero_dir):
    
    if file.is_file():
        filename = file.name

        with open(file.path, "r") as f:
            new_lines = []

            line = f.readline()
            while line != '':
                
                if re.search("boundaryField", line):
                    new_lines.append(line)
                    line = f.readline()
                    new_lines.append(line)
                    new_lines.append("\t#includeEtc \"caseDicts/setConstraintTypes\"\n")
                    line = f.readline()

                
                elif re.search("domain", line):
                    if re.search("k|omega", filename):
                        sub("type fixedValue", "\t\ttype slip;\n", True)
                            

                    elif re.search("nut", filename):
                        sub("type zeroGradient", "\t\ttype calculated;\n")
                        new_lines.append("\t\tvalue uniform 0.;\n")
                

                    elif re.search("U", filename):
                        sub("type surfaceNormalFixedValue", "\t\ttype slip;\n", True)
    

                    elif re.search("p", filename):
                        sub("type zeroGradient", "\t\ttype slip;\n")


                elif re.search("outlet|ground", line) and re.search("U", filename):
                    sub("value", f"\t\tvalue uniform ({speed}. 0. 0.);\n")

                elif re.search("internalField", line) and re.search("U", filename):
                    line = f"internalField uniform ({speed}. 0. 0.);\n"

                elif re.search("entrata.+no_layer|uscita.+no_layer", line):

                    if re.search("k|omega", filename):
                        for new_line in new_lines:
                            if re.search("internalField", new_line):
                                val = re.search("[0-9\.]+", new_line).group()
                        if re.search("entrata", line):
                            sub("type", f"\t\ttype inletOutlet;\n\t\tvalue uniform {val};\n\t\tinletValue uniform {val};\n", skipline=True)
                        elif re.search("uscita", line):
                            sub("type", f"\t\ttype fixedValue;\n\t\tvalue uniform {val};\n", skipline=True)

                    elif re.search("nut", filename):
                        sub("type", "\t\ttype calculated;\n\t\tvalue uniform 0.;\n")

                new_lines.append(line)
                line = f.readline()            

 
        with open(file.path, "w") as f:
            for line in new_lines:
                f.write(line)

for file in os.scandir(system_dir):
    if file.name == "fvSolution":
        os.remove(file)


with open(system_dir / "controlDict", "r") as c:
    line = c.readline()
    
    while line != "":
        if re.search("patches", line):
            line = c.readline()
            alette, muro, flap = check_am()
        line = c.readline()


with open(system_dir / "controlDict", "r") as c:
    new_lines = []

    line = c.readline()
    while line != '':

        if re.search("functions", line):
            new_lines.append(line)
            new_lines.append("\n")
            for file in os.scandir(general_fun_dir):
                if file.is_file():
                    copy(file.path, system_dir)
                    if (file.name != "functionTimeControl") and (file.name != "fvSolution"):
                        new_lines.append(f"\t#include \"{file.name}\"\n")

            if alette:
                for file in os.scandir(wing_functions_dir):
                    if re.search("Flap", file.name) and not flap:
                        continue
                    copy(file.path, system_dir)
                    new_lines.append(f"\t#include \"{file.name}\"\n")
            
            if muro:
                for file in os.scandir(wall_functions_dir):
                    copy(file.path, system_dir)
                    new_lines.append(f"\t#include \"{file.name}\"\n")

            new_lines.append("\n")

            while not re.search("residuals", line):
                line = c.readline()
        
        elif re.search("patches", line):
            new_lines.append(line)
            line = c.readline()
            enlist_patches("ground")

        elif re.search("dragDir", line):
            new_lines.append("\t\tdragDir (-1. 0. 0.);\n")
            line = c.readline()

        elif re.search("endTime.*[0-9]+", line):
            endtime = int(re.search("[0-9]+", line).group())

        new_lines.append(line)
        line = c.readline()

with open(system_dir / "controlDict", "w") as control:
    for line in new_lines:
        control.write(line)


if alette:
    patches = ""
    for item in alette:
        patches = patches + item + " "
        if re.search("main", item):
            mainwing = item
        elif re.search("endplate", item):
            endplate = item

    with open(system_dir / "forcesAlette", "r") as al:
        new_lines = []

        line = al.readline()
        while line != '':
            if re.search("^\tpatches", line):
                line = f"\tpatches\t({patches});"
            new_lines.append(line)
            line = al.readline()
    
    with open(system_dir / "forcesAlette", "w") as al:
        for line in new_lines:
            al.write(line)

    with open(system_dir / "forcesMainWing", "r") as al:
        new_lines = []

        line = al.readline()
        while line != '':
            if re.search("^\tpatches", line):
                line = f"\tpatches\t({mainwing});"
            new_lines.append(line)
            line = al.readline()
    
    with open(system_dir / "forcesMainwing", "w") as al:
        for line in new_lines:
            al.write(line)

    with open(system_dir / "forcesEndplate", "r") as al:
        new_lines = []

        line = al.readline()
        while line != '':
            if re.search("^\tpatches", line):
                line = f"\tpatches\t({endplate});"
            new_lines.append(line)
            line = al.readline()
    
    with open(system_dir / "forcesEndplate", "w") as al:
        for line in new_lines:
            al.write(line)

    if flap:
        with open(system_dir / "forcesFlap", "r") as al:
            new_lines = []

            line = al.readline()
            while line != '':
                if re.search("^\tpatches", line):
                    line = f"\tpatches\t({flap});"
                new_lines.append(line)
                line = al.readline()
    
        with open(system_dir / "forcesFlap", "w") as al:
            for line in new_lines:
                al.write(line)
        
with open(system_dir / "functionTimeControl", "r") as F:
    new_lines = F.readlines()

    for i in range(len(new_lines)):
        if re.search("timeEnd", new_lines[i]):
            new_lines[i] = f"timeEnd {str(endtime)};\n"

with open(system_dir / "functionTimeControl", "w") as timeF:
    for line in new_lines:
        timeF.write(line)


with open(system_dir / "fieldAverage", "r") as fA:
    new_lines = fA.readlines()

    for i in range(len(new_lines)):
        if re.search("timeStart", new_lines[i]):
            new_lines[i] = f"\ttimeStart\t{str(endtime-250)};\n"

with open(system_dir / "fieldAverage", "w") as fA:
    for line in new_lines:
        fA.write(line)

with open(system_dir / "forcesCarena", "r") as forces:
    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("^\tpatches", line):
            line = "\tpatches\t\t(\n"
            new_lines.append(line)
            for patch in carena:
                line = f"\t\t\t{patch}\n"
                new_lines.append(line)
            
            line = "\t\t\t\t);\n"
        
        new_lines.append(line)
        line = forces.readline()

with open(system_dir / "forcesCarena", "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(system_dir / "forcesParafango", "r") as forces:
    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("^\tpatches", line):
            line = "\tpatches\t\t(\n"
            new_lines.append(line)
            for patch in paraf_ant:
                line = f"\t\t\t{patch}\n"
                new_lines.append(line)
            
            line = "\t\t\t\t);\n"

        new_lines.append(line)
        line = forces.readline()

with open(system_dir / "forcesParafango", "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(system_dir / "forcesParafPost", "r") as forces:
    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("^\tpatches", line):
            line = "\tpatches\t\t(\n"
            new_lines.append(line)
            for patch in paraf_post:
                line = f"\t\t\t{patch}\n"
                new_lines.append(line)
            
            line = "\t\t\t\t);\n"

        new_lines.append(line)
        line = forces.readline()

with open(system_dir / "forcesParafPost", "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(system_dir / "forcesPilota", "r") as forces:

    patches = ""
    for item in pilota:
        patches = patches + item + " "

    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("^\tpatches", line):
            new_lines.append(f"\tpatches\t ({patches}casco);\n")
        
        else: new_lines.append(line)
        line = forces.readline()

with open(system_dir / "forcesPilota", "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(system_dir / "globalForces", "r") as gforces:
    new_lines = []

    line = gforces.readline()
    while line != '':
        if re.search("^\tpatches", line):
            new_lines.append(line)
            for patch in patches_list:
                new_lines.append(patch)
        else: new_lines.append(line)
        line = gforces.readline()

with open(system_dir / "globalForces", "w") as gforces:
    for line in new_lines:
        gforces.write(line)