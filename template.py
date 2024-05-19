import os 
from pathlib import Path
import logging


# logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

while True:
    project_name=input("Enter your folder name: ")
    if project_name!="":
        break


list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/logger/__init__.py",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html",
    "main.py"
]

for filespath in list_of_files:
    filespath=Path(filespath)
    filedir,filename=os.path.split(filespath)

    if filedir !="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory:(filedir) for the file: (filename)")
    
    if (not os.path.exists(filespath) or (os.path.getsize) == 0):
        with open(filespath ,'w') as f:
            pass
            logging.info(f"Creating empty file:{filespath}")
    else:
        logging.info(f"{filename} is already exists")