# Add your utilities or helper functions to this file.

import os
import glob
import shutil
from dotenv import load_dotenv, find_dotenv

def remove_files_from_folder(folder_pattern):
    app_folders = glob.glob(folder_pattern)
    [shutil.rmtree(app_folder) for app_folder in app_folders if os.path.exists(app_folder)]

def load_env():
    _ = load_dotenv(find_dotenv())
    remove_files_from_folder("app*")  

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


