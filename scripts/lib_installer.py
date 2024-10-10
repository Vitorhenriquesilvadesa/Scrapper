import os
import importlib.util
from typing import List
from colorama import Fore, Style, init

def verify_install(libs: List):
    
    all_installs_done = True
    
    for name in libs:
        
        spec = importlib.util.find_spec(name)    
            
        if spec is None:
            print(f"{Style.BRIGHT}{Fore.RED}{name} {Style.NORMAL}{Fore.RESET}is not installed.")
            all_installs_done = False
            
        else:
            print(f"{Style.BRIGHT}{Fore.BLUE}{name} {Style.NORMAL}{Fore.RESET}is already installed.")
            
    return all_installs_done

def install_libs(libs):
   
    os.system("clear")
    
    for name in libs:
        
        spec = importlib.util.find_spec(name)    
            
        if spec is None:
            os.system(f"pip install {name}")
            
        else:
            print(f"{Fore.BLUE}{name} is already installed.")

def run(lib_names: List):
    
    os.system("clear")
        
    if not verify_install(libs=lib_names):
        response = input("Proceed to instalation of not found packages? Y/N")
        
        if response == "Y":
            install_libs(libs=lib_names)

        else:
            exit()

    os.system("pip freeze > requirements.txt")