import pandas as pd
import os
import shutil
import ntpath
from venv import create
import subprocess
import matplotlib.pyplot as plt


def is_valid_file(parser, arg):
    if isinstance(arg, str):
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return arg
    elif isinstance(arg, list):
        for a in arg:
            if not os.path.exists(a):
                parser.error("The file %s does not exist!" % a)
        return arg

def copy_file(copy_from, copy_to_folder):
    copy_to = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'analyses', copy_to_folder))
    if not os.path.exists(copy_to):
        os.makedirs(copy_to)
    shutil.copy2(copy_from, copy_to) 
    return os.path.join(copy_to, ntpath.split(copy_from)[1])

def create_venv(save_dirpath, folder_name, requirements_file_path):
    venv_dir = os.path.join(save_dirpath, folder_name, 'venv')
    create(venv_dir, with_pip=True)

    python_exe = os.path.join("Scripts", "python.exe")
    subprocess.run([os.path.join(venv_dir, python_exe), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([os.path.join(venv_dir, python_exe), "-m", "pip", "install", "-r", requirements_file_path], check=True)
	
def save_dataframe(df, storage_path, file_name):
    # Saves a dataframe as a csv in the folder specified in file_folder.
    #storage_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'analyses', relative_path))
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    df.to_csv(os.path.join(storage_path, file_name), index=False)

def save_plot(storage_path, file_name):
    # Saves a plot into the folder specified in file_folder. Format can be changed e.g. svg, jpeg, png.
    #storage_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'analyses', relative_path))
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    plt.savefig(os.path.join(storage_path, file_name), dpi=300, bbox_inches = "tight", format='png')
    return os.path.join(storage_path, file_name)
    #plt.show()

