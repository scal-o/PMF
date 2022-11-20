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

        elif re.search("alette", patch):
            if alette == False:
                alette = []
            alette.append(patch.strip("\t\n"))
        elif re.search("muro", patch):
            muro = True

        elif re.search("pilota", patch):
            pilota = True
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

    
print("\nScript to create 0/ and system/ dirs")

default = ""
flag = False
while default == "" or flag == False:

    try:
        default = input("\nShould default data for relTol and speed be used? (y/n): ").lower()
    except: 
        print("\nPlease only insert y or n as an answer")

    if default == "y":
        relTol = "1e-4"
        speed = "-50"
        flag = True

    elif default == "n":
        while True:
            relTol = input("\nrelTol (default 1e-4): ")
            if re.search("[1-9]+e\-[1-9]+0?$", relTol):
                break
            else: print("\nInvalid input. Correct format: 1e-4")
        
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

                new_lines.append(line)
                line = f.readline()            

 
        with open(file.path, "w") as f:
            for line in new_lines:
                f.write(line)

with open(os.path.join(system_dir, "controlDict"), "r") as c:
    new_lines = []

    line = c.readline()
    while line != '':

        if re.search("functions", line):
            new_lines.append(line)
            new_lines.append("\n")
            for file in os.scandir(general_fun_dir):
                copy(file.path, system_dir)
                if file.name != "functionTimeControl":
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
            endtime = re.search("[0-9]+", line).group()

        new_lines.append(line)
        line = c.readline()

with open(os.path.join(system_dir, "controlDict"), "w") as control:
    for line in new_lines:
        control.write(line)


with open(os.path.join(system_dir, "functionTimeControl"), "r") as F:
    new_lines = F.readlines()

    for i in range(len(new_lines)):
        if re.search("timeEnd", new_lines[i]):
            new_lines[i] = "timeEnd " + str(endtime) + ";\n"

with open(os.path.join(system_dir, "functionTimeControl"), "w") as timeF:
    for line in new_lines:
        timeF.write(line)


with open(os.path.join(system_dir, "fvSolution"), "r") as fv:
    new_lines = []

    line = fv.readline()
    while line != '':

        if re.search("relTol", line):
            new_lines.append(f"\trelTol\t\t {relTol};\n")
        else:
            new_lines.append(line)
        
        line = fv.readline()

with open(os.path.join(system_dir, "fvSolution"), "w") as fvSolution:
    for line in new_lines:
        fvSolution.write(line)


with open(os.path.join(system_dir, "forcesCarena"), "r") as forces:
    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("patches", line):
            line = "\tpatches\t\t(\n"
            new_lines.append(line)
            for patch in carena:
                line = f"\t\t\t{patch}\n"
                new_lines.append(line)
            
            line = "\t\t\t\t);\n"
        
        new_lines.append(line)
        line = forces.readline()

with open(os.path.join(system_dir, "forcesCarena"), "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(os.path.join(system_dir, "forcesParafango"), "r") as forces:
    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("patches", line):
            line = "\tpatches\t\t(\n"
            new_lines.append(line)
            for patch in paraf_ant:
                line = f"\t\t\t{patch}\n"
                new_lines.append(line)
            
            line = "\t\t\t\t);\n"

        new_lines.append(line)
        line = forces.readline()

with open(os.path.join(system_dir, "forcesParafango"), "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(os.path.join(system_dir, "forcesParafPost"), "r") as forces:
    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("patches", line):
            line = "\tpatches\t\t(\n"
            new_lines.append(line)
            for patch in paraf_post:
                line = f"\t\t\t{patch}\n"
                new_lines.append(line)
            
            line = "\t\t\t\t);\n"

        new_lines.append(line)
        line = forces.readline()

with open(os.path.join(system_dir, "forcesParafPost"), "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(os.path.join(system_dir, "forcesPilota"), "r") as forces:
    new_lines = []

    line = forces.readline()
    while line != '':
        if re.search("patches", line):
            new_lines.append("\tpatches\t (pilota casco);\n")
        
        else: new_lines.append(line)
        line = forces.readline()

with open(os.path.join(system_dir, "forcesPilota"), "w") as forces:
    for line in new_lines:
        forces.write(line)


with open(os.path.join(system_dir, "globalForces"), "r") as gforces:
    new_lines = []

    line = gforces.readline()
    while line != '':
        if re.search("^\tpatches", line):
            new_lines.append(line)
            for patch in patches_list:
                new_lines.append(patch)
        else: new_lines.append(line)
        line = gforces.readline()

with open(os.path.join(system_dir, "globalForces"), "w") as gforces:
    for line in new_lines:
        gforces.write(line)