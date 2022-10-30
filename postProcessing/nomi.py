from asyncio.windows_events import NULL
import os,re
cwd = os.getcwd()

part_list = []
path_list = []

for root, dirs, files in os.walk(os.path.join(cwd, "postProcessing")):
    for i in range(len(dirs)):
        if re.search("[Ff]orces", dirs[i]):
            part_list.append(re.sub("[Ff]orces", "", dirs[i]))
    for file in files:
        if re.search("forces.dat", file):
            path_list.append(os.path.join(root, file))


    
    
    
    '''for i in range(len(dirs)):
        if re.search("[Ff]orces", dirs[i]):
            part_list.append(re.sub("[Ff]orces", "", dirs[i]))
            for entry in os.scandir(os.path.join(root, dirs[i])):
                print(entry)
                if entry.is_file():
                    path_list.append(entry.path)'''


print(part_list)
print(path_list)