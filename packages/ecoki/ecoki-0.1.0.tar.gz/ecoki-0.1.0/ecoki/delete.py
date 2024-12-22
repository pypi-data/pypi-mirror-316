# write a script to list all names of the folders inside the folder "ecoki/piplines" and save the list to a file named "pipeline_names.txt".
import os

def list_pipeline_folders():
    """
    Lists all names of the folders inside the folder "pipelines" and saves the list to a file named "pipeline_names.txt".

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    pipeline_folder_path = 'pipelines/ecoki_pipelines'
    pipeline_folder_path_2 = 'pipelines/custom_pipelines'
    folder_names = [name for name in os.listdir(pipeline_folder_path) if os.path.isdir(os.path.join(pipeline_folder_path, name))]
    folder_names_2 = [name for name in os.listdir(pipeline_folder_path_2) if os.path.isdir(os.path.join(pipeline_folder_path_2, name))]
    folder_names = folder_names + folder_names_2
    
    with open('pipeline_names.txt', 'w') as file:
        for folder_name in folder_names:
            file.write(f"{folder_name}\n")
            
def list_building_block_folders():
    """
    Lists all names of the folders inside the folder "building_blocks/code_based" recursively,
    excluding the root folder name, any '__pycache__' folders, and sub root folders like 'data_integration'.
    The list is saved to a file named "building_block_names.txt".

    This function traverses the directory structure starting from 'building_blocks/code_based',
    listing all subdirectories (excluding '__pycache__' directories and sub root folders) and writes them to 'building_block_names.txt' file.

    Parameters
    ----------
    None

    Returns
    -------
    list
        A list of relative paths to all folders found within the root directory, excluding the root folder name, any '__pycache__' folders, and sub root folders.
    """
    root_folder_path = 'building_blocks/code_based'
    exclude_folders = ['__pycache__', 'code_based']  # Add sub root folders to exclude here
    folder_names = []

    for root, dirs, files in os.walk(root_folder_path):
        dirs[:] = [d for d in dirs if d not in exclude_folders]  # Exclude specified folders from dirs
        for name in dirs:
            folder_path = os.path.join(root, name)
            if os.path.isdir(folder_path):
                relative_path = os.path.relpath(folder_path, root_folder_path)
                if relative_path != '.' and all(sub_root not in relative_path.split(os.path.sep) for sub_root in exclude_folders):
                    folder_names.append(relative_path)

    with open('building_block_folder_names.txt', 'w') as file:
        for folder_name in sorted(folder_names):
            file.write(f"{folder_name}\n")
            
    return sorted(folder_names)


import pandas as pd

def check_readme_in_folders():
    """
    Checks if folders returned from list_building_block_folders() contain a README file.
    Saves the results as a DataFrame and a CSV file with columns: {folder_name, README status (boolean)}.

    Parameters
    ----------
    None

    Returns
    -------
    DataFrame
        A DataFrame containing the folder names and a boolean indicating the presence of a README file.
    """
    building_block_folders = list_building_block_folders()
    root_folder_path = 'building_blocks/code_based'
    readme_status = []

    for folder in building_block_folders:
        folder_path = os.path.join(root_folder_path, folder)
        readme_file = any(file for file in os.listdir(folder_path) if file.lower().startswith('readme'))
        readme_status.append({'folder_name': folder, 'README status': readme_file})

    readme_df = pd.DataFrame(readme_status)
    readme_df.to_csv('readme_status.csv', index=False)

    return readme_df


def list_python_modules_exclude_interactive_gui():
    """
    Lists all Python modules in the folders returned by list_building_block_folders(), excluding any named "interactive_gui".

    Parameters
    ----------
    None

    Returns
    -------
    list
        A list of paths to Python modules, excluding those named "interactive_gui".
    """
    building_block_folders = list_building_block_folders()
    root_folder_path = 'building_blocks/code_based'
    python_modules = []

    for folder in building_block_folders:
        folder_path = os.path.join(root_folder_path, folder)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py") and not file.startswith("interactive_gui") and not file.startswith("__init__"):
                    relative_path = os.path.relpath(os.path.join(root, file), root_folder_path)
                    if relative_path not in python_modules:  # Check to avoid duplicates
                        python_modules.append(relative_path)
    with open('building_block_names.txt', 'w') as file:  # Corrected file name to reflect content
        for module_path in sorted(python_modules):
            file.write(f"{module_path}\n")  # Corrected to write module paths instead of list repr

    return python_modules

import pymongo

def collect_and_save_db_collections_as_csv(mongo_uri):
    """
    Connects to the MongoDB instance using the provided URI, collects the names of all databases and their collections,
    and saves them into a CSV file named 'mongodb_dbs_collections.csv'.

    Parameters
    ----------
    mongo_uri : str
        The MongoDB URI to connect to.

    Returns
    -------
    None
    """
    client = pymongo.MongoClient(mongo_uri)
    dbs = client.list_database_names()
    db_collections = []

    for db_name in dbs:
        db = client[db_name]
        collections = db.list_collection_names()
        for collection in collections:
            db_collections.append({'database': db_name, 'collection': collection})

    db_collections_df = pd.DataFrame(db_collections)
    db_collections_df.to_csv('mongodb_dbs_collections.csv', index=False)

    print(f"Collected and saved {len(db_collections)} database-collection pairs to mongodb_dbs_collections.csv")



if __name__ == '__main__':
    #list_pipeline_folders()
    #list_building_block_folders()
    #list_python_modules_exclude_interactive_gui()
    #check_readme_in_folders()
    collect_and_save_db_collections_as_csv("mongodb://141.76.56.139:27017/")
