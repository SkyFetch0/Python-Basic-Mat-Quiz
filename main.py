import tkinter as tk
from quiz_app import MathQuizApp
from config import APP_SETTINGS
import requests
from colorama import Fore,Back,Style
import git
import shutil
import os
import sys
def check_libraries():
    required_libraries = {
        'tkinter': 'GUI için temel kütüphane',
        'random': 'Rastgele sayı üretimi için',
        'threading': 'Zamanlayıcı için',
        'json': 'JSON dosyası okuma için',
        'operator': 'Matematik operatörleri için',
        'math': 'Matematik fonksiyonları için',
        'requests': "Güncelleme Ve Get istekler için"
    }

    missing_libraries = []
    installed_libraries = []

    print(Fore.GREEN + "Kütüphane Kontrol Ediliyor...")
    print("-" * 50)

    for library, description in required_libraries.items():
        try:
            __import__(library)
            installed_libraries.append(f"✓ {library}: {description}")
        except ImportError:
            missing_libraries.append(f"✗ {library}: {description}")

    print("Yüklü Kütüphaneler:")
    for lib in installed_libraries:
        print(Fore.YELLOW + lib)

    if missing_libraries:
        print(Fore.RED+"\nEksik Kütüphaneler:")
        for lib in missing_libraries:
            print(lib)
        print("\nEksik kütüphaneleri yüklemek için:")
        for lib in missing_libraries:
            lib_name = lib.split(':')[0].replace('✗ ', '')
            print(f"pip install {lib_name}")
    else:

        print(Fore.GREEN + "\nTüm gerekli kütüphaneler yüklü!")
        return True

def update_system():
    print(Fore.YELLOW + "Sistem Güncelleniyor..." + Fore.RESET)
    path = os.path.dirname(__file__) + "/"
    backup_folder = path + "backup/"
    os.makedirs(backup_folder, exist_ok=True)
    print(os.listdir(backup_folder))
    config = path + "config.py"
    # Old Backup Code

    #mains = path + "main.py"
    #math_operations = path + "math_operation.py"
    #quiz_app = path + "quiz_app.py"
    #utils = path + "utils.py"
    #config = path + "config.py"

    #shutil.copy(mains, backup_folder)
    #shutil.copy(math_operations, backup_folder)
    #shutil.copy(quiz_app, backup_folder)
    #shutil.copy(utils, backup_folder)
    #shutil.copy(utils, backup_folder)

        #New Backup Code
    backup_files = ['main.py','math_operation.py','quiz_app.py','utils.py','config.py']
    for file in backup_files:
        if os.path.exists(path + file):
            shutil.copy(path + file, backup_folder)

    repo_url = "https://github.com/SkyFetch0/Python-Basic-Mat-Quiz"
    local_path = path + "update"
    os.makedirs(local_path, exist_ok=True)
    repo = git.Repo.clone_from(repo_url, local_path)
    print(f"Güncel Dosyalar indi konum: " + local_path)
    
    shutil.move(local_path,path)

    print(Fore.GREEN + " Başarıyla Güncelleme Yapıldı! Uygulama Yeniden Başlatılıyor!" + Fore.RESET)
    os.execv(sys.executable, ['python'] + sys.argv)




def check_update():

    response = requests.get(APP_SETTINGS['UPDATE_SERVER'])
    data = response.json()
    version = data['version']
    if APP_SETTINGS['APP_VERSION'] != version and APP_SETTINGS['APP_VERSION'] < version:
        print(Fore.RED + "Versiyon Güncel Değil!")
        update_system()
    else:
        print(Fore.GREEN + "Versiyon Güncel!")

    print(Fore.RESET + "Versiyon: " + Fore.YELLOW+ str(APP_SETTINGS['APP_VERSION']) + Fore.RESET)



def main():
    check = check_libraries()
    check_update()


if __name__ == "__main__":
    main()