import os, shutil, pathlib, re

# script to test the functionality of run.py etc

cwd = os.getcwd()
cwd = pathlib.Path(cwd)

for obj in os.scandir(cwd):
    if obj.is_dir() and re.search("prima_copy", obj.name):
        shutil.rmtree(obj.path)

shutil.copytree(cwd / "sim_scripts" / "prima", cwd / "prima_copy")
shutil.copytree(cwd / "sim_scripts" / "postProcessing", cwd / "prima_copy" / "postProcessing")

os.mkdir(cwd / "prima_copy" / "results")

for obj in os.scandir(cwd / "sim_scripts"):
    if obj.is_file() and re.search("\.py$", obj.name):
        shutil.copy(obj.path, cwd / "prima_copy")

os.chdir(cwd / "prima_copy")
run = cwd / "prima_copy" / "run.py"
exec(open(run).read())